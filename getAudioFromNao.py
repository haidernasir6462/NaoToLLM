from naoqi import ALProxy

# Create proxies to connect to the robot's speech recognition and memory modules
speech_recognition = ALProxy("ALSpeechRecognition", "<nao_ip>", 9559)
memory = ALProxy("ALMemory", "<nao_ip>", 9559)

# Enable the recognition engine
speech_recognition.setLanguage("English")
speech_recognition.setVocabulary(["yes", "no", "start", "stop"], False)
speech_recognition.subscribe("Test_ASR")

def on_speech_detected(value):
    print("Command received: ", value)

# Subscribe to the "WordRecognized" event in memory to get the detected words
memory.subscribeToEvent("WordRecognized", "<your_module>", "on_speech_detected")
