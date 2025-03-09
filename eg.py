import yt_dlp
import subprocess
import os
import logging

def download_instagram_audio(instagram_url, output_mp3_file="output_audio1.mp3"):
    try:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Download best audio format
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_video.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([instagram_url])

        # Find downloaded file
        downloaded_file = None
        for filename in os.listdir():
            if filename.startswith('downloaded_video.'):
                downloaded_file = filename
                break

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

# Example usage
if __name__ == "__main__":  
    download_instagram_audio("https://www.instagram.com/p/DGxS1PBCPHR")
