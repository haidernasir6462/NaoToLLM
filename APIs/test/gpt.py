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

    def onInput_onStart(self):
        # Simple print to test if requests is available
        print("Starting to send request...")

        try:
            # Define the URL of the Ollama server API
            url = 'http://192.168.138.153:11434/api/generate'
            
            # Define the payload (you can customize this based on your API)
            payload = {
                "model": "llama3.1",
                'prompt': 'Hello, NAO robot here! What should I do?'
            }
            
            # Test if the requests module works
            self.tts.say("Sending request to server")

            # Send the request to the Ollama server
            response = requests.post(url, json=payload, stream=True)  # Using stream=True to handle multiple JSON objects
            
            self.tts.say("Received response from server")

            # Initialize an empty string to hold the final response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode and parse each JSON object
                        response_data = json.loads(line.decode('utf-8'))
                        response_text = response_data.get('response', '')
                        if response_text:  # Check if response_text is not empty
                            full_response += response_text  # Accumulate the text
                    except json.JSONDecodeError as e:
                        print("JSON decode error:", e)
                        self.tts.say("Error parsing JSON")

            # Ensure full_response is not empty
            if full_response.strip():  # Check if full_response has any content
                self.tts.say("Response from server: " + full_response)
            else:
                self.tts.say("No valid response from server.")

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
