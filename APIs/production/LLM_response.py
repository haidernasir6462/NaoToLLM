import requests
from naoqi import ALProxy
import json

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages

    def onUnload(self):
        # Clean-up code
        pass

    def onInput_onStart(self, p):
        print("Starting to send request...")
        prompt= str(p)
        self.tts.say(prompt)
        try:
            # Define the URL of the Ollama server API
            url = 'http://192.168.203.153:11434/api/generate'
            
            # Define the payload (you can customize this based on your API)
            payload = {
                "model": "llama3.1",
                'prompt': prompt
            }
            
            # Test if the requests module works
            self.tts.say("Sending request to server")

            # Send the request to the Ollama server
            response = requests.post(url, json=payload, stream=False)
                
            if response.status_code == 200:
            
                full_response = ""
                # Parse the JSON response, extract the actual response
                raw_data = response.text.strip().splitlines()
                for item in raw_data:
                    parsed_item = json.loads(item)
                    response_value = parsed_item.get('response')
                    response_value += " "
                    full_response += response_value  # Accumulate the text
                    
                self.tts.say(str(full_response))

            else:
                self.tts.say("Failed to fetch a response. Status code: " + str(response.status_code))

        except Exception as e:
            # Catching any exception and reporting it using TTS
            error_message = "Exception: {0}".format(str(e))
            print(error_message)  # Log the error message for debugging
            self.tts.say(error_message)

        # Activate the output of the box
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload()  # Clean-up when the box is stopped
        self.onStopped()  # Activate the output of the box