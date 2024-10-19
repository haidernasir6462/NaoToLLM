# Example usage:
from APIs.test.ollamaResponse import get_ollama_response
from APIs.test.speechToText import transcribe_audio


file_path = '20230607_me_canadian_wildfires.mp3'
transcribeText = transcribe_audio(file_path)
print("got transcribed text")
response = get_ollama_response("give me one line summary of this text" + transcribeText)
print(response)