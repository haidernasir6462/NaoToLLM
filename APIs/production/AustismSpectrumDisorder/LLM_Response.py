import requests
from naoqi import ALProxy
import json

class MyClass(GeneratedClass):
    def __init__(self):
        # Correct __init__ method with double underscores
        GeneratedClass.__init__(self)
        self.conversation_history = []  # Initialize the conversation history as a list
        self.full_query = ""  # To store the final query
        self.user_attributes = None  # To store the input from input_1
        self.user_question = None  # To store the input from onStart

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages

    def onUnload(self):
        # Clean-up code
        pass

    def onInput_input_1(self, attributes):
        # Store the input from the attributes box
        self.user_attributes = str(attributes)
        self.full_query += " The attributes of the user are " + str(self.user_attributes)

        # Check if both inputs have arrived
        self.process_if_ready()
        self.onStopped()

    def onInput_onStart(self, p):
        # Store the input from the question box
        self.user_question = str(p)
        self.full_query += " The question is: " + self.user_question + ". Give me short and personalized answer based on the attributes of the user and dont mention anything about the attributes in the response"

        # Check if both inputs have arrived
        self.process_if_ready()
        self.onStopped()

    def process_if_ready(self):
        """Process the inputs if both inputs have been received."""
        if self.user_attributes is not None and self.user_question is not None:
            # Both inputs have been received, proceed with sending the request to the Ollama server

            # Add the user's message to the conversation history
            self.conversation_history.append({
                "role": "user",
                "content": self.full_query
            })

            try:
                # Define the URL of the Ollama server API
                url = 'http://192.168.155.153:11434/api/chat'

                # Prepare the payload for Ollama including the conversation history
                payload = {
                    "model": "llama3.1",
                    "messages": self.conversation_history  # Send the conversation history
                }

                self.tts.say("Please wait while I am processing.")
                print("Final query before processing: " + self.full_query)
                self.tts.say("Final query before processing: " + self.full_query)
                print(payload)
                print(self.full_query)

                # Send the request to the Ollama server
                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    full_response = ""
                    # Parse the JSON response
                    raw_data = response.text.strip().splitlines()
                    for item in raw_data:
                        parsed_item = json.loads(item)
                        message = parsed_item.get('message', {})
                        response_value = message.get('content', "")
                        full_response += response_value  # Accumulate the text
    
                    self.tts.say(str(full_response.strip()))  # Speak the accumulated text
    
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": full_response.strip()
                    })
                # Activate the output of the box

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