# 🎶 YouTube Audio Extractor 🎶

## 🚀 Blast Off!

Ever find a song on YouTube that you just *have* to have on your MP3 player? Well, you're in luck! This nifty little Python script will snatch the audio from any YouTube video and save it as a glorious MP3 file. 🎧

## 🛠️ For the Developers (aka The Mad Scientists)

If you want to tinker with the code or just get it running on your local machine, follow these steps.

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

### 3. Install the Goodies

This project has a few dependencies. Let's get them installed.

```bash
pip install -r requirements.txt
```

### 4. Get `ffmpeg`

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

### 5. Configure `ffmpeg`

Now, we need to tell the script where to find `ffmpeg`. Open up `main.py` and find this section:

```python
'ffmpeg_location': 'C:/Users/maxeg/Downloads/ffmpeg-7.1.1-full_build/ffmpeg-7.1.1-full_build/bin'
```

Replace the path with the path to your `ffmpeg` bin directory.

## 👨‍🎤 For the End Users (aka The Rockstars)

Ready to rock? Here's how to use the script.

### On Windows (PowerShell)

```powershell
.\venv\Scripts\python.exe main.py "YOUR_YOUTUBE_URL_HERE"
```

### On Windows (Git Bash) / macOS / Linux

```bash
python main.py "YOUR_YOUTUBE_URL_HERE"
```

### Optional: Specify an Output Directory

By default, your MP3s will be saved in a directory called `output`. If you want to save them somewhere else, use the `-o` or `--output` flag.

```bash
python main.py "YOUR_YOUTUBE_URL_HERE" -o "C:\Users\YourUser\Music"
```

And that's it! Enjoy your new MP3s! 🎉
