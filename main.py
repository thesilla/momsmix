import argparse
import os
import yt_dlp
from pydub import AudioSegment

def download_video(url, output_path):
    """Downloads the YouTube video from the given URL."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'C:/Users/maxeg/Downloads/ffmpeg-7.1.1-full_build/ffmpeg-7.1.1-full_build/bin'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        return os.path.join(output_path, f"{title}.mp3"), title

def main():
    """Main function to run the YouTube to MP3 converter."""
    parser = argparse.ArgumentParser(description="Download audio from a YouTube video and save it as an MP3.")
    parser.add_argument("url", help="The URL of the YouTube video.")
    parser.add_argument("-o", "--output", default="output", help="The output directory to save the MP3 file.")
    
    args = parser.parse_args()
    
    try:
        # Ensure the output directory exists
        if not os.path.exists(args.output):
            os.makedirs(args.output)
            
        download_video(args.url, args.output)
        print("Successfully downloaded and converted video to MP3.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
