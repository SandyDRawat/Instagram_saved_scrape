import yt_dlp
import subprocess
import os
import logging
import asyncio
import pandas as pd
from shazamio import Shazam

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def detect_song(audio_file):
    """Recognizes the song using Shazam."""
    try:
        shazam = Shazam()
        result = await shazam.recognize_song(audio_file)
        return result
    except Exception as e:
        logging.error(f"Shazam error: {e}")
        return None

def download_instagram_audio(instagram_url, output_mp3_file="output_audio.mp3"):
    """Downloads Instagram video audio and converts it to MP3."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_video.%(ext)s',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([instagram_url])

        # Find downloaded file
        downloaded_file = next((f for f in os.listdir() if f.startswith('downloaded_video.')), None)
        if not downloaded_file:
            logging.error("Downloaded video file not found.")
            return None

        # Convert to MP3
        subprocess.run([
            'ffmpeg', '-i', downloaded_file, '-vn', '-b:a', '192k', output_mp3_file
        ], check=True, capture_output=True)

        logging.info(f"MP3 audio saved as: {output_mp3_file}")
        return output_mp3_file
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg error: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None

def process_song(audio_file):
    """Runs Shazam detection and returns song details."""
    loop = asyncio.get_event_loop()
    song_info = loop.run_until_complete(detect_song(audio_file))

    if song_info and "track" in song_info:
        track = song_info["track"]
        return {
            "Title": track.get("title", "Unknown"),
            "Artist": track.get("subtitle", "Unknown"),
           # "Shazam URL": track.get("share", {}).get("href", "N/A")
        }
    return {"Title": "Not Found", "Artist": "Not Found", "Shazam URL": "N/A"}

def main(input_csv, output_csv):
    """Reads Instagram links from CSV, processes them, and saves song info."""
    df = pd.read_csv(input_csv)
    results = []

    for index, row in df.iterrows():
        instagram_url = row.get("link")
        if not instagram_url:
            continue

        logging.info(f"Processing: {instagram_url}")

        audio_file = download_instagram_audio(instagram_url, output_mp3_file=f"audio_{index}.mp3")
        if audio_file:
            song_data = process_song(audio_file)
            song_data["Instagram_Link"] = instagram_url
            results.append(song_data)

    # Save results to a new CSV
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    logging.info(f"Results saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    main("D:/projects/song_extractor/instagram-saved-scraper/output.csv", "output_songs.csv")
