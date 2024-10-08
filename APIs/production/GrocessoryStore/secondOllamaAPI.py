import requests
from naoqi import ALProxy
import json

class MyClass(GeneratedClass):
    def __init__(self):
        # Correct __init__ method with double underscores
        GeneratedClass.__init__(self)
        self.conversation_history = []  # Initialize the conversation history as a list
        self.query = ""
    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")  # Use TTS to speak messages
            
    def onUnload(self):
        # Clean-up code
        pass
    
    def onInput_input_1(self, full_query):
#        self.tts.say("received query is " + str(full_query))

        # Concatenate to self.query instead of append
        self.query += "customers query is " + str(full_query)
#        self.tts.say(self.query)

        self.onStopped()

    def onInput_onStart(self, p):
        product = str(p)  # Get the user's input
        self.query += " and product detail is " + product

        # Add the user's message to the conversation history
        self.conversation_history.append({
            "role": "user",
            "content": "give me short and concise response of customer query. " + self.query
        })

        # Example message to demonstrate the working list
#        self.tts.say("User input has been added to history")

        try:
            # Define the URL of the Ollama server API
            url = 'http://192.168.76.153:11434/api/chat'

            # Prepare the payload for Ollama including the conversation history
            payload = {
                "model": "llama3.1",
                "messages": self.conversation_history  # Send the conversation history
            }

            self.tts.say("Please wait while i am processing for second round to ollama.")
#            self.tts.say("Respond according to question." + self.query)

            
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

        
        self.onStopped()

    def onInput_onStop(self, full_query):
        
        self.onUnload()  # Clean up when the box is stopped
        self.onStopped()  # Activate the output of the box