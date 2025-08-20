import argparse
import os
import yt_dlp
from pydub import AudioSegment

def download_video(url, output_path, download_video=False):
    """Downloads the YouTube video or audio from the given URL."""
    if download_video:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ffmpeg_location': 'C:/Users/maxeg/Downloads/ffmpeg-7.1.1-full_build/ffmpeg-7.1.1-full_build/bin'
        }
    else:
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
        ext = 'mp4' if download_video else 'mp3'
        return os.path.join(output_path, f"{title}.{ext}"), title

def main():
    """Main function to run the YouTube to MP3 converter."""
    parser = argparse.ArgumentParser(description="Download audio or video from a YouTube video.")
    parser.add_argument("url", help="The URL of the YouTube video.")
    parser.add_argument("-o", "--output", default="output", help="The output directory to save the file.")
    parser.add_argument("-v", "--video", action="store_true", help="Download the video instead of extracting the audio.")
    
    args = parser.parse_args()
    
    try:
        # Ensure the output directory exists
        if not os.path.exists(args.output):
            os.makedirs(args.output)
            
        download_video(args.url, args.output, args.video)
        if args.video:
            print("Successfully downloaded video.")
        else:
            print("Successfully downloaded and converted video to MP3.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
