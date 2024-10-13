import requests
import time

# Replace with your actual API key from AssemblyAI
API_KEY = 'cfb3686fbcc14f08a67d576d3c63d29f'

# Upload audio file to AssemblyAI
def upload_audio(file_path):
    headers = {
        'authorization': API_KEY
    }

    # Open the audio file in binary mode
    with open(file_path, 'rb') as audio_file:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            files={'file': audio_file}
        )

    # Check if upload was successful
    if response.status_code == 200:
        return response.json()['upload_url']
    else:
        raise Exception('Audio upload failed. Status code: ', response.status_code)

# Send the uploaded audio for transcription
def request_transcription(upload_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    
    json_data = {
        "audio_url": upload_url
    }

    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(endpoint, json=json_data, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception('Transcription request failed. Status code: ', response.status_code)

# Get the transcription result
def get_transcription_result(transcript_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    
    headers = {
        "authorization": API_KEY
    }

    while True:
        response = requests.get(endpoint, headers=headers)

        # If transcription is complete, return it
        if response.status_code == 200:
            transcript_data = response.json()
            if transcript_data['status'] == 'completed':
                return transcript_data['text']
            elif transcript_data['status'] == 'failed':
                raise Exception('Transcription failed.')
        else:
            raise Exception('Failed to retrieve transcription result. Status code: ', response.status_code)

        # Wait a few seconds before checking again
        # print("waiting for 5 seconds")
        time.sleep(10)

# Full function to transcribe audio
def transcribe_audio(file_path):
    upload_url = upload_audio(file_path)
    transcript_id = request_transcription(upload_url)
    transcription_text = get_transcription_result(transcript_id)
    return transcription_text


