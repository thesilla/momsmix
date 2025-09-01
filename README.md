# 🎶 YouTube to Firebase Audio Uploader 🎶

## 🚀 Overview

This Python script automates the process of extracting audio from YouTube videos and linking them to a Firestore database. It reads a `songs` collection in Firestore, and for each song that has a `youtubelink` and no `audiofile`, it downloads the audio, converts it to MP3, and uploads it to Firebase Storage. Finally, it updates the song document with a public URL to the newly uploaded audio file.

## 🛠️ Setup and Configuration

Follow these steps to get the script running on your local machine.

### 1. Create a Virtual Environment

It's always a good idea to keep your Python projects in their own little sandboxes.

**On Windows (PowerShell):**
```powershell
python -m venv venv
```

**On macOS/Linux (Bash):**
```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

Now, let's step into our new sandbox.

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**On Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**On macOS/Linux (Bash):**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

This project has a few dependencies. Let's get them installed.

```bash
pip install -r requirements.txt
```

### 4. Set Up Firebase

This script requires a Firebase project to function.

1.  **Create a Firebase Project**: If you don't already have one, create a new project in the [Firebase Console](https://console.firebase.google.com/).
2.  **Create a Service Account**:
    *   In your Firebase project, go to **Project settings** > **Service accounts**.
    *   Click **Generate new private key**. This will download a JSON file.
    *   Rename the downloaded file to `serviceAccountKey.json` and place it in the root directory of this project.
3.  **Set IAM Permissions**:
    *   Go to the [Google Cloud Console IAM page](https://console.cloud.google.com/iam-admin/iam).
    *   Find the service account you just created (the email address is in the `serviceAccountKey.json` file).
    *   Click the **Edit** button (pencil icon).
    *   Click **Add another role** and add the **Cloud Datastore User** role. This allows the script to read from your Firestore database.
    *   Ensure the service account also has a role that allows writing to Storage, such as **Storage Object Admin**.
4.  **Configure Storage Bucket**:
    *   In the `main.py` file, find the following line:
        ```python
        'storageBucket': 'your-storage-bucket-name.appspot.com'
        ```
    *   Replace `'your-storage-bucket-name.appspot.com'` with your actual Firebase Storage bucket name. You can find this in the **Storage** section of the Firebase Console.

### 5. Get `ffmpeg`

This is the magic wand that does the audio conversion.

**On Windows:**
The easiest way is to download it directly.
1.  Grab the latest release from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z).
2.  Extract the `.7z` file (you might need [7-Zip](https://www.7-zip.org/)).
3.  Make a note of the path to the `bin` directory inside the extracted folder. You'll need it for the next step.

**On macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**On Linux (using apt):**
```bash
sudo apt-get install ffmpeg
```

### 6. Configure `ffmpeg`

Now, we need to tell the script where to find `ffmpeg`. Open up `main.py` and find this section:

```python
'ffmpeg_location': 'C:/Users/maxeg/Downloads/ffmpeg-7.1.1-full_build/ffmpeg-7.1.1-full_build/bin'
```

Replace the path with the path to your `ffmpeg` bin directory.

## 🚀 Running the Script

Once everything is configured, you can run the script in one of two modes.

### Processing from Firestore

To process the songs from your Firestore collection, run the script without any arguments:

```bash
python main.py
```

The script will read your Firestore `songs` collection, process any songs that have a `youtubelink` but no `audiofile`, and upload the extracted audio to Firebase Storage, linking it back to the song document.

### Processing a Single URL

You can also process a single YouTube URL directly from the command line.

**To download audio:**

```bash
python main.py --url "https://www.youtube.com/watch?v=your-video-id"
```

**To download the video:**

```bash
python main.py --url "https://www.youtube.com/watch?v=your-video-id" --video-only
```

## 🔥 Adding Songs to Process

To add a song to the processing queue, add a new document to your `songs` collection in Firestore. The document should contain a field named `youtubelink`:

*   **Field Name**: `youtubelink`
*   **Field Type**: `string`
*   **Field Value**: `https://www.youtube.com/watch?v=your-video-id`

The script will automatically process any new songs that have a `youtubelink` and do not yet have an `audiofile` field.

And that's it! Enjoy your automated audio uploader! 🎉
