import time
import requests
from naoqi import ALProxy
import json

class MyClass(GeneratedClass):
    def _init_(self):
        GeneratedClass._init_(self)

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages

        pass

    def onUnload(self):
        # Clean-up code here
        pass

    def onInput_onStart(self):
        # Localize the variables to avoid attribute conflicts
        api_url = "https://api.assemblyai.com/v2/transcript"
        api_key = "57d2a68a356d43a597b482db470becbf"
        audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

        # Send the POST request and wait for the response
        transcript_id = self.send_post_request(api_url, api_key, audio_url)

        if transcript_id:
            # Poll for the transcription status
            transcript = self.poll_transcription_status(api_url, api_key, transcript_id)
            if transcript:
                a = transcript['text']
                print "Transcription response:", a
            else:
                print "Failed to retrieve the transcription."
        else:
            print "Failed to get a response from the API."

        self.onStopped()

    def onInput_onStop(self):
        self.onUnload()  # Clean up when stopped
        self.onStopped()  # Trigger next behavior

    def send_post_request(self, api_url, api_key, audio_url):
        """Send the POST request to AssemblyAI API and return the transcript ID."""
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "audio_url": audio_url
        }

        try:
            print "Sending POST request to AssemblyAI..."
            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 200:
                transcript_data = response.json()
                return transcript_data['id']  # Return the transcript ID for polling
            else:
                print "Failed with status code {}: {}".format(response.status_code, response.text)
                return None

        except requests.RequestException as e:
            print "An error occurred while sending the request: {}".format(e)
            return None

    def poll_transcription_status(self, api_url, api_key, transcript_id):
        """Poll the transcription status until it is completed."""
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

        while True:
            time.sleep(5)  # Wait for 5 seconds before polling
            response = requests.get("{}/{}".format(api_url, transcript_id), headers=headers)

            if response.status_code == 200:
                transcript_data = response.json()
                status = transcript_data['status']
                print "Current status:", status

                if status == 'completed':
                    return transcript_data  # Return the completed transcript data
                elif status == 'failed':
                    print "Transcription failed."
                    return None
            else:
                print "Failed to poll with status code {}: {}".format(response.status_code, response.text)
                return None