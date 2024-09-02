import speech_recognition as sr

def convert_wav_to_text(wav_file_path):
    """
    Converts a WAV audio file to text using Google Web Speech API.

    :param wav_file_path: str, path to the WAV file
    :return: str, transcribed text from the audio
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    try:
        # Recognize the speech in the audio file using Google Web Speech API
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
