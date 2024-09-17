from pydub import AudioSegment
import math
import os

# Function to split audio into chunks
def split_audio(file_path, chunk_length_ms, output_folder="audio_chunks"):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculate the number of chunks
    total_length_ms = len(audio)
    num_chunks = math.ceil(total_length_ms / chunk_length_ms)

    # Split and save chunks
    for i in range(num_chunks):
        start = i * chunk_length_ms
        end = min((i + 1) * chunk_length_ms, total_length_ms)
        
        chunk = audio[start:end]
        chunk_name = f"{output_folder}/chunk_{i+1}.wav"
        
        # Export chunk as WAV file
        chunk.export(chunk_name, format="wav")
        print(f"Exported {chunk_name}")

# Example usage
file_path = "IslahiMajlis.wav"  # Replace with your audio file path
chunk_length_ms = 300000  # 5 minutes chunk size (in milliseconds)
split_audio(file_path, chunk_length_ms)
