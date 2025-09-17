import os
import yt_dlp
import firebase_admin
import argparse
import threading
import time
from firebase_admin import credentials, firestore, storage

callback_done = threading.Event()

def initialize_firebase():
    """Initializes the Firebase Admin SDK."""
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'gillman-music.firebasestorage.app'  # Replace with your storage bucket name
    })

def download_media(url, output_path, video_only=False):
    """Downloads media from the given YouTube URL."""
    if video_only:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'ffmpeg_location': 'C:/Users/maxeg/Downloads/ffmpeg-7.1.1-full_build/ffmpeg-7.1.1-full_build/bin'
        }
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
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
        ext = 'mp3' if not video_only else info_dict.get('ext', 'mp4')
        return os.path.join(output_path, f"{title}.{ext}"), title

def upload_to_storage(file_path, file_name):
    """Uploads a file to Firebase Storage and returns its public URL."""
    bucket = storage.bucket()
    blob = bucket.blob(f"audio/{file_name}.mp3")
    blob.upload_from_filename(file_path)
    blob.make_public()
    print(f"Uploaded {file_name}.mp3 to Firebase Storage.")
    return blob.public_url

def on_snapshot(doc_snapshot, changes, read_time):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            song_data = change.document.to_dict()
            if song_data.get('youtubelink') and not song_data.get('audiofile'):
                print(f"New song detected: {song_data.get('name')}")
                try:
                    audio_file, title = download_media(song_data.get('youtubelink'), output_dir)
                    if audio_file and os.path.exists(audio_file):
                        public_url = upload_to_storage(audio_file, title)
                        change.document.reference.update({'audiofile': public_url})
                        os.remove(audio_file)
                        print(f"Successfully processed and uploaded {title}.mp3")
                    else:
                        print(f"Failed to download audio from {song_data.get('youtubelink')}")
                except Exception as e:
                    print(f"An error occurred while processing {song_data.get('youtubelink')}: {e}")
    callback_done.set()

def watch_songs():
    initialize_firebase()
    db = firestore.client()
    songs_ref = db.collection('songs')
    songs_ref.on_snapshot(on_snapshot)
    print("Watching for new songs...")
    while True:
        time.sleep(1)

def main():
    """Main function to process YouTube videos from Firebase."""
    parser = argparse.ArgumentParser(description="Download YouTube media or process a Firestore collection.")
    parser.add_argument('--url', type=str, help='A single YouTube URL to process.')
    parser.add_argument('--video-only', action='store_true', help='Download the video instead of extracting audio. Requires --url.')
    parser.add_argument('--watch', action='store_true', help='Watch for new songs in the Firestore collection.')
    args = parser.parse_args()

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if args.watch:
        watch_songs()
    elif args.url:
        print(f"Processing single URL: {args.url}")
        media_file, title = download_media(args.url, output_dir, args.video_only)
        if media_file and os.path.exists(media_file):
            print(f"Successfully downloaded {title} to {media_file}")
        else:
            print(f"Failed to download media from {args.url}")
    else:
        initialize_firebase()
        db = firestore.client()
        
        songs_ref = db.collection('songs')
        docs = songs_ref.stream()

        for doc in docs:
            song_data = doc.to_dict()
            if song_data.get('audiofile'):
                print(f"Skipping song: {song_data.get('name')} (audiofile already exists)")
                continue
            
            url = song_data.get('youtubelink')
            if url:
                try:
                    print(f"Processing song: {song_data.get('name')}")
                    audio_file, title = download_media(url, output_dir)
                    if audio_file and os.path.exists(audio_file):
                        public_url = upload_to_storage(audio_file, title)
                        doc.reference.update({'audiofile': public_url})
                        os.remove(audio_file)
                        print(f"Successfully processed and uploaded {title}.mp3")
                    else:
                        print(f"Failed to download audio from {url}")
                except Exception as e:
                    print(f"An error occurred while processing {url}: {e}")

if __name__ == "__main__":
    main()
