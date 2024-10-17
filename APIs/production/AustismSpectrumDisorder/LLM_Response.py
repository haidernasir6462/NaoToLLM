import requests
from naoqi import ALProxy
import json

class MyClass(GeneratedClass):
    def __init__(self):
        # Correct __init__ method with double underscores
        GeneratedClass.__init__(self)
        self.conversation_history = []  # Initialize the conversation history as a list
        self.full_query = ""  # Change full_query to an instance variable

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages

    def onUnload(self):
        # Clean-up code
        pass

    def onInput_input_1(self, attributes):
        attributes = str(attributes)
        self.full_query += " The attributes of user are " + str(attributes)  # Corrected to use "are"

        self.onStopped()

    def onInput_onStart(self, p):
        user_input = str(p)  # Get the user's input
        self.full_query += "The question is: " + user_input

        # Add the user's message to the conversation history
        self.conversation_history.append({
            "role": "user",
            "content": self.full_query + " give just a few lines answer"
        })

        # Example message to demonstrate the working list
        # self.tts.say("User input has been added to history")

        try:
            # Define the URL of the Ollama server API
            url = 'http://192.168.152.153:11434/api/chat'

            # Prepare the payload for Ollama including the conversation history
            payload = {
                "model": "llama3.1",
                "messages": self.conversation_history  # Send the conversation history
            }

            self.tts.say("Please wait while I am processing.")
            print("final query before processing is" + self.full_query)
            self.tts.say("final query before processing is" + self.full_query)
            # Send the request to the Ollama server
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                full_response = ""
                self.tts.say("Received response")

                # Parse the JSON response
                raw_data = response.json()  # Use json() to directly decode the JSON response
                if isinstance(raw_data, list):  # Ensure the response is a list
                    for item in raw_data:
                        message = item.get('message', {})
                        response_value = message.get('content', "")
                        full_response += response_value + " "  # Accumulate the text

                self.tts.say(str(full_response.strip()))  # Speak the accumulated text
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response.strip()
                })

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
        self.onUnload()  # Clean up when the box is stopped
        self.onStopped()  # Activate the output of the box