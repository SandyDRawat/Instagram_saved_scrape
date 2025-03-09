import base64
import requests

def convert_raw_to_base64(input_raw_file, output_txt_file):
    try:
        with open(input_raw_file, 'rb') as raw_file:
            raw_audio_data = raw_file.read()
        
        encoded_text = base64.b64encode(raw_audio_data).decode('utf-8')
        
        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            txt_file.write(encoded_text)
        
        print(f"Base64 encoding saved to: {output_txt_file}")
        return encoded_text
    
    except Exception as e:
        print(f"Error encoding file: {e}")
        return None

def get_song_info(encoded_audio_txt):
    try:
        url = "https://shazam.p.rapidapi.com/songs/detect"

        payload = encoded_audio_txt
        headers = {
            "x-rapidapi-key": "b6881f77b4mshb5aef39281c9d5ep110ab1jsn60ca109eaff6",
            "x-rapidapi-host": "shazam.p.rapidapi.com",
            "Content-Type": "text/plain"
        }

        response = requests.post(url, data=payload, headers=headers)
        print(response)
        if response.status_code == 200:
            data = response.json()
            
            # Extract song title and artist name
            song_title = data.get("track", {}).get("title", "Unknown")
            artist_name = data.get("track", {}).get("subtitle", "Unknown")

            return {
                "title": song_title,
                "artist": artist_name
            }
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    except Exception as e:
        print(f"Error getting song info: {e}")
        return None


if __name__ == "__main__":
    encoded_audio = convert_raw_to_base64("D:/projects/song_extractor/instagram-saved-scraper/raw_audio.raw", "encoded_audio.txt")
    song_info = get_song_info(encoded_audio)
    print(song_info)
