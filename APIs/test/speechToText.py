import speech_recognition as sr

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.audio_file_path = '/home/nao/recordings/microphones/test.wav'  # Define the path to your audio file

    def onLoad(self):
        # Initialization code
        pass

    def onUnload(self):
        # Clean-up code
        pass


    def access_recorded_audio(self):
        # Open and read the recorded file
        try:
            with open(self.audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                # Do something with the audio data (e.g., analyze it)
                print("Successfully accessed the recorded audio.")
                # Example: print first 100 bytes (if it's not too large)
                print(audio_data[:100])
        except IOError as e:
            print("Failed to access the recorded audio file: {0}".format(e))
    def audio_to_text(self):
        # Initialize recognizer
        recognizer = sr.Recognizer()

        try:
            # Load audio file
            with sr.AudioFile(self.audio_file_path) as source:
                audio = recognizer.record(source)

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio"
        except sr.RequestError as e:
            return "Could not request results from Google Web Speech API; {0}".format(e)
        except Exception as e:
            return "An error occurred: {0}".format(e)

    def onInput_onStart(self, p):

#        print("receiving the audio file")
#        audio = p
#        self.tts.say(audio)
        # Process the audio and print the text
#        text = self.audio_to_text()
        print("Converted Text:", text)
        # Activate the output of the box
        # self.onStopped() # Uncomment this if needed

    def onInput_onStop(self):
        self.onUnload()  # Reuse the clean-up as the box is stopped
        self.onStopped()  # Activate the output of the box