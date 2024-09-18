import os
import time
from naoqi import ALProxy

class MyClass(GeneratedClass):
    def _init_(self):
        GeneratedClass._init_(self)

    def onLoad(self):
        # Initialization code
        self.tts = ALProxy("ALTextToSpeech")
        self.audio_recorder = ALProxy("ALAudioRecorder")
        self.audio_player = ALProxy("ALAudioPlayer")  # Proxy for playing the recorded audio
        self.audio_path = "/home/nao/recordings/microphones/test.wav"  # Path to save the recorded audio

    def onUnload(self):
        # Clean-up code
        pass

    def onInput_onStart(self):
        # Start recording audio
        self.tts.say("I'm listening. Please speak.")
        self.startRecording()

        # Wait for 5 seconds (or you can implement a better method to detect the end of speech)
        time.sleep(5)

        # Stop recording
        self.tts.say("Recording complete.")
        self.stopRecording()

        # NAO speaks and plays back the recorded audio
        self.tts.say("I will now play what you said.")
        self.playRecordedAudio()

        # Activate the output of the box
        self.onStopped()

    def startRecording(self):
        """Start the audio recording."""
        channels = [0, 0, 1, 0]  # Enable only the front microphone
        self.audio_recorder.startMicrophonesRecording(self.audio_path, "wav", 16000, channels)

    def stopRecording(self):
        """Stop the audio recording."""
        self.audio_recorder.stopMicrophonesRecording()

    def playRecordedAudio(self):
        """Play the recorded audio using NAO's speakers."""
        try:
            self.audio_player.playFile(self.audio_path)  # Play the recorded WAV file
        except Exception as e:
            error_message = "Error playing the recorded audio: {0}".format(str(e))
            print(error_message)
            self.tts.say(error_message)

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()