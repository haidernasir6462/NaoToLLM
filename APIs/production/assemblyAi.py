import time
import requests
from naoqi import ALProxy
import json
import os

class MyClass(GeneratedClass):
    def _init_(self):
        GeneratedClass._init_(self)
        self.audio_file_path = '/home/nao/recordings/microphones/test.wav'  # Update with your audio file path

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages
        self.audio_player = ALProxy("ALAudioPlayer")  # Proxy for playing the recorded audio

    def onUnload(self):
        # Clean-up code here
        pass

    def onInput_onStart(self, p ):
        self.tts.say("I have received the recording. I am going to play it")
        self.audio_player.playFile(p)  # Play the recorded WAV file

        # Localize the variables to avoid attribute conflicts
        upload_url = "https://api.assemblyai.com/v2/upload"
        transcript_url = "https://api.assemblyai.com/v2/transcript"
        api_key = "57d2a68a356d43a597b482db470becbf"

        # Step 1: Upload the audio file
        audio_url = self.upload_audio(upload_url, api_key, p)

        if audio_url:
            # Step 2: Request transcription
            transcript_id = self.request_transcription(transcript_url, api_key, audio_url)

            if transcript_id:
                # Step 3: Poll for the transcription status
                transcript = self.poll_transcription_status(transcript_url, api_key, transcript_id)
                if transcript:
                    text = transcript['text']
                    print("Transcription response:", text)
                    self.tts.say(str(text))  # NAO speaks the transcribed text
                    # NAO sends the audio to the next box
                    
                    self.tts.say("I am going to send the recording to the next box.")
                    self.SendTranscribedTextToLLama(str(text))
                    self.tts.say("Recording sent successfully by output 1.")
                    
                else:
                    print("Failed to retrieve the transcription.")
            else:
                print("Failed to get a response from the transcription request.")
        else:
            print("Failed to upload audio.")

        self.onStopped()
        
    def SendTranscribedTextToLLama(self,Transcribedtext):
        """Send the transcribed text to the next box."""
        try:
            self.output_1(Transcribedtext)  # Send the audio to the next box through output_1
        except Exception as e:
            error_message = "Error sending Transcribed text: {0}".format(str(e))
            print(error_message)
            self.tts.say(error_message)
    
        pass

    def onInput_onStop(self):
        self.onUnload()  # Clean up when stopped
        self.onStopped()  # Trigger next behavior

    def upload_audio(self, upload_url, api_key, audio_file_path):
        """Upload the audio file to AssemblyAI and return the audio URL."""
        headers = {
            "authorization": api_key,
        }

        with open(audio_file_path, 'rb') as audio_file:
            response = requests.post(upload_url, headers=headers, data=audio_file)

        if response.status_code == 200:
            upload_response = response.json()
            return upload_response['upload_url']  # Return the uploaded audio URL
        else:
            print("Failed to upload audio with status code {}: {}".format(response.status_code, response.text))
            return None

    def request_transcription(self, transcript_url, api_key, audio_url):
        """Send the POST request to AssemblyAI API for transcription and return the transcript ID."""
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "audio_url": audio_url
        }

        try:
            print("Sending transcription request to AssemblyAI...")
            response = requests.post(transcript_url, headers=headers, json=data)

            if response.status_code == 200:
                transcript_data = response.json()
                return transcript_data['id']  # Return the transcript ID for polling
            else:
                print("Failed with status code {}: {}".format(response.status_code, response.text))
                return None

        except requests.RequestException as e:
            print("An error occurred while sending the request: {}".format(e))
            return None

    def poll_transcription_status(self, transcript_url, api_key, transcript_id):
        """Poll the transcription status until it is completed."""
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

        while True:
            time.sleep(5)  # Wait for 5 seconds before polling
            response = requests.get("{}/{}".format(transcript_url, transcript_id), headers=headers)

            if response.status_code == 200:
                transcript_data = response.json()
                status = transcript_data['status']
                print("Current status:", status)

                if status == 'completed':
                    return transcript_data  # Return the completed transcript data
                elif status == 'failed':
                    print("Transcription failed.")
                    return None
            else:
                print("Failed to poll with status code {}: {}".format(response.status_code, response.text))
                return None