# Assuming you have the converted text in a variable named 'converted_text'
from APIs.getResponseFromLLMgenerateAPI import generate_response
from SpeechToText import convert_wav_to_text

if __name__ == "__main__":
    wav_file_path = "whatIsYoutube.wav"
    converted_text = convert_wav_to_text(wav_file_path)
    print("Transcribed Text:", converted_text)

if converted_text: 
    api_response = generate_response(converted_text)

if api_response:
    print("API Response:", api_response)
