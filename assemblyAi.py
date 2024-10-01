import assemblyai as aai
import time

# Set your API key
aai.settings.api_key = "57d2a68a356d43a597b482db470becbf"

def upload_audio(file_path):
    """
    Uploads an audio file to AssemblyAI and returns the upload URL.
    """
    print(f"Uploading {file_path} for transcription...")
    upload_response = aai.Transcriber().upload(file_path)
    return upload_response['upload_url']

def transcribe_audio(upload_url):
    """
    Submits the audio file for transcription and waits for the result.
    """
    print("Requesting transcription...")
    transcriber = aai.Transcriber()
    
    # Start the transcription process
    transcript = transcriber.transcribe(audio_url=upload_url)

    # Wait for the transcription to complete
    while transcript['status'] not in ['completed', 'failed']:
        print(f"Status: {transcript['status']}... waiting...")
        time.sleep(5)  # Polling interval to check the status again
        transcript = transcriber.get_transcript(transcript['id'])

    if transcript['status'] == 'completed':
        print("Transcription completed successfully!")
        return transcript['text']
    else:
        raise Exception("Transcription failed")

def main():
    # Path to your audio file
    audio_file_path = "whatIsYoutube.wav"
    
    # Step 1: Upload the audio file to AssemblyAI
    audio_url = upload_audio(audio_file_path)
    
    # Step 2: Transcribe the uploaded audio
    transcription = transcribe_audio(audio_url)
    
    # Print the transcribed text
    print("Transcribed Text:")
    print(transcription)

if __name__ == "__main__":
    main()
