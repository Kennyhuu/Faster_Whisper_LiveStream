

# YouTube Livestream Transcriber with Whisper

This Python script captures the audio stream of a YouTube livestream and transcribes (and optionally translates) it in real time using:

- [`yt_dlp`](https://github.com/yt-dlp/yt-dlp) for extracting the livestream audio URL
- [`ffmpeg`](https://ffmpeg.org/) for audio processing
- 
On windows install ffmpeg
https://phoenixnap.com/kb/ffmpeg-windows

- [`faster-whisper`](https://github.com/guillaumekln/faster-whisper) for speech transcription
- `numpy` for handling audio data

## 📦 Requirements

Install the required Python packages:

```bash
pip install yt-dlp ffmpeg-python numpy faster-whisper

⚙️ Configuration
YouTube URL: Change the livestream link directly in the __main__ section.

Language: Specify the spoken language using ISO codes (e.g., "ja" for Japanese, "en" for English).

The Whisper task is set to "translate" – it will always output English.