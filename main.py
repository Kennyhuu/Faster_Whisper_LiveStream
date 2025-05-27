import subprocess
import numpy as np
from faster_whisper import WhisperModel


model = WhisperModel("base", device="cpu", compute_type="int8")

youtube_url = "https://www.youtube.com/watch?v=O_1z0UhvY2Y&ab_channel=CeciliaImmergreenCh.hololive-EN"
# Step 1: get direct audio url using yt-dlp
proc = subprocess.run(["yt-dlp", "-f", "bestaudio", "-g", youtube_url], capture_output=True, text=True)
audio_url = proc.stdout.strip()
print(f"Audio URL: {audio_url}")

# Step 2: Run ffmpeg to pipe raw audio
ffmpeg_cmd = [
    "ffmpeg",
    "-loglevel", "error",
    "-i", audio_url,
    "-f", "s16le",    # raw pcm 16-bit little endian
    "-ar", "16000",   # 16kHz sample rate
    "-ac", "1",       # mono
    "-"
]

ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, bufsize=10**8)

chunk_size = 16000 * 2 * 5  # 5 seconds audio: sample_rate * bytes_per_sample * seconds

try:
    while True:
        in_bytes = ffmpeg_proc.stdout.read(chunk_size)
        if len(in_bytes) == 0:
            print("Stream ended")
            break

        # Convert to numpy float32 array normalized -1 to 1
        audio = np.frombuffer(in_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        # Transcribe with Faster Whisper
        segments, info = model.transcribe(audio, beam_size=5, language="en", task="translate")

        text = "".join([seg.text for seg in segments]).strip()
        if text:
            print(f">>> {text}")

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    ffmpeg_proc.kill()
