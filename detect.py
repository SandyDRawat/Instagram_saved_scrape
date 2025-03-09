import asyncio
from shazamio import Shazam

async def detect_song(audio_file):
    shazam = Shazam()
    result = await shazam.recognize_song(audio_file)
    return result

def main(audio_file):
    loop = asyncio.get_event_loop()
    song_info = loop.run_until_complete(detect_song(audio_file))

    if "track" in song_info:
        track = song_info["track"]
        print(f"🎵 Song: {track['title']}")
        print(f"👨‍🎤 Artist: {track['subtitle']}")
        print(f"🔗 Shazam URL: {track['share']['href']}")
    else:
        print("❌ No song detected. Try a different audio sample.")

# Example Usage
if __name__ == "__main__":
    main("D:/projects/song_extractor/instagram-saved-scraper/output_audio1.mp3")  # Replace with your audio file path
