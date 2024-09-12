import requests
from naoqi import ALProxy
import json
import sys

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.tts = None

    def onLoad(self):
        # Initialization code
        try:
            self.tts = ALProxy("ALTextToSpeech")
            print("Successfully connected to ALTextToSpeech")
            
            # Check and set language if needed
            current_language = self.tts.getLanguage()
            print("Current TTS language:", current_language)
            # Uncomment the next line if you need to set a specific language
            # self.tts.setLanguage("English")
            
            # Reset voice parameters
            self.tts.setParameter("pitchShift", 1.0)
            self.tts.setParameter("doubleVoice", 0.0)
        except Exception as e:
            print("Error initializing ALTextToSpeech:", str(e))
            sys.exit(1)

    def onUnload(self):
        # Clean-up code
        self.tts = None

    def safe_say(self, message):
        """Safely use TTS to speak a message."""
        try:
            if not isinstance(message, str) or not message.strip():
                raise ValueError("Message must be a non-empty string")
            self.tts.say(message)
        except Exception as e:
            print("TTS Error:", str(e))
            self.tts.say("I encountered an error while speaking.")

    def onInput_onStart(self):
        print("Starting to send request...")

        try:
            # Define the URL of the Ollama server API
            url = 'http://192.168.138.153:11434/api/generate'
            
            # Define the payload
            payload = {
                "model": "llama3.1",  # Make sure this matches your server's model name
                'prompt': 'Hello, NAO robot here! What should I do?'
            }
            
            self.safe_say("Sending request to server")

            # Send the request to the Ollama server
            response = requests.post(url, json=payload, timeout=30)
            
            self.safe_say("Received response from server")

            # Print raw response text for debugging
            print("Response Text:", response.text)
            
            # Parse the response
            try:
                response_data = json.loads(response.text)
                full_response = response_data.get('response', '')
                
                if full_response.strip():
                    self.safe_say("Response from server: " + full_response)
                else:
                    self.safe_say("No valid response from server.")
            except json.JSONDecodeError as e:
                print("JSON decode error:", str(e))
                self.safe_say("Error parsing server response")

        except requests.exceptions.RequestException as e:
            error_message = "Network error: {0}".format(str(e))
            print(error_message)
            self.safe_say(error_message)
        except Exception as e:
            error_message = "Unexpected error: {0}".format(str(e))
            print(error_message)
            self.safe_say(error_message)

        # Activate the output of the box
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload()  # Clean-up when the box is stopped
        self.onStopped()  # Activate the output of the box