from pydub import AudioSegment
import numpy as np

def convert_mp3_to_raw(input_mp3, output_raw):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_mp3)
    
    # Convert to the required format (44100Hz, Mono, 16-bit PCM)
    audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)  # 2 bytes = 16-bit PCM
    
    # Get raw audio data as bytes
    raw_data = np.array(audio.get_array_of_samples(), dtype=np.int16).tobytes()
    
    # Save raw data to file
    with open(output_raw, "wb") as raw_file:
        raw_file.write(raw_data)

# Example usage
convert_mp3_to_raw("D:/projects/song_extractor/instagram-saved-scraper/output_audio.mp3", "output.raw")
