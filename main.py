# Assuming you have the converted text in a variable named 'converted_text'
from APIs.getResponsefromLLM import generate_response
from SpeechToText import convert_wav_to_text

if __name__ == "__main__":
    wav_file_path = "whatIsYoutube.wav"
    converted_text = convert_wav_to_text(wav_file_path)
    print("Transcribed Text:", converted_text)

api_response = generate_response(converted_text)

if api_response:
    print("API Response:", api_response)
    # You can access the generated response from the API response
    generated_text = api_response["generated_text"]
    print("Generated Text:", generated_text)