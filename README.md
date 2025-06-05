

# 🎙️ YouTube Livestream Transcriber with Whisper

This Python script captures the audio stream of a YouTube livestream and transcribes it (and optionally translates it to English) in real time using:

- [`yt_dlp`](https://github.com/yt-dlp/yt-dlp) for extracting the livestream audio URL
- [`ffmpeg`](https://ffmpeg.org/) for audio processing
On windows install ffmpeg
https://phoenixnap.com/kb/ffmpeg-windows

- [`faster-whisper`](https://github.com/guillaumekln/faster-whisper) for speech transcription
- `numpy` for handling audio data

## 📦 Requirements

Install the required Python packages:
- via requirment.txt

## or

```bash
pip install yt-dlp ffmpeg-python numpy faster-whisper

⚙️ Configuration
YouTube URL: Change the livestream link directly in the __main__ section.

Language: Specify the spoken language using ISO codes (e.g., "ja" for Japanese, "en" for English).

The Whisper task is set to "translate" – it will always output English.
```

## ⚡ GPU Acceleration (Optional)
To run faster-whisper on a CUDA-enabled GPU:

Install the CUDA Toolkit

Install the correct version of PyTorch with CUDA support:

Example (for CUDA 11.8):

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


# Then, make sure your model is initialized with:
model = WhisperModel("base", device="cuda", compute_type="float32")

```
## ⚙️ Configuration
Modify the following inside the script:

YouTube URL
Set the livestream link in the __main__ or pass it to get_youtube_livestream_url(...).

Language
Define the spoken language using ISO 639-1 codes, e.g.,:

"en" for English

"ja" for Japanese

"es" for Spanish

Transcription Mode
The task is set to "translate" by default, which always outputs English. To transcribe in the original language, change it to "transcribe":

```bash
segments, _ = model.transcribe(
    audio,
    beam_size=10,
    vad_filter=True,
    language=language,
    task="translate"  # or "transcribe"
)
```

```bash
youtube_url = "https://www.youtube.com/watch?v=LIVE_STREAM_ID"
language = "ja"  # Language spoken in the livestream
yt_audio_url = get_youtube_livestream_url(youtube_url)
get_recording_and_transrecord(yt_audio_url, language)
```

## 📝 Notes
This works only with active livestreams, not past or upcoming videos.

Audio is processed in ~5-second chunks using VAD to skip silence.

Basic reconnection handling (reconnect()) is a placeholder – you may extend it for fault tolerance.

For improved accuracy, you can switch to a larger Whisper model like "medium" or "large-v3".

## TODO
 - Improve translation using LLM model
 - create an UI interface for ouput
 - create a reconnect