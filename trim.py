import ffmpeg

def trim_mp3(input_mp3, output_mp3, start_time=0, duration=5):
    """
    Trims an MP3 file from `start_time` to `start_time + duration`.
    
    Args:
        input_mp3 (str): Path to the input MP3 file.
        output_mp3 (str): Path to save the trimmed MP3.
        start_time (int/float): Start time in seconds.
        duration (int/float): Duration of the trimmed clip in seconds.
    """
    (
        ffmpeg.input(input_mp3, ss=start_time, t=duration)
        .output(output_mp3, format='mp3')
        .run(overwrite_output=True)
    )

# Example usage: Trim the first 5 seconds from input.mp3
trim_mp3("D:/projects/song_extractor/instagram-saved-scraper/output_audio1.mp3", "output_audio.mp3", start_time=0, duration=3)
