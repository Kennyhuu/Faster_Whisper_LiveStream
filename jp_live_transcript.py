
from yt_dlp import YoutubeDL
import ffmpeg
import numpy as np
from faster_whisper import WhisperModel

#Default model = WhisperModel("base", device="cpu", compute_type="int8")
model = WhisperModel("large-v3", device="cuda", compute_type="float32")


def get_youtube_livestream_url(youtube_url: str):
    """
    Extracts the direct audio stream URL from a YouTube livestream.

    Args:
        youtube_url (str): The YouTube livestream URL.

    Returns:
        str: Direct audio stream URL.
    """
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'skip_download': True,
        'forceurl': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']
        print(f"Audio URL: {audio_url}")

    return audio_url


def reconnect():
    pass


def get_recording_and_transrecord(yt_audio_link: str, language: str):
    """
    Streams audio using ffmpeg, converts it, and transcribes it using Whisper.

    Args:
    yt_audio_link (str): The direct audio URL from YouTube.
    language (str): The language spoken in the audio (e.g., 'ja', 'en').
    """
    try:
        process = (
            ffmpeg
            .input(yt_audio_link, loglevel="error")
            .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )
    except Exception as e:
        print("Failed to open ffmpeg stream:", str(e))
        exit()
    # Default chunk_size = 16000 * 2 * 5  # 5 seconds audio: sample_rate * bytes_per_sample * seconds
    chunk_size = 16000 * 2 * 10  # 5 seconds of 16kHz mono 16-bit

    try:
        while True:
            in_bytes = process.stdout.read(chunk_size)
            if not in_bytes:
                print("No more audio. Stream ended.")
                break

            audio = np.frombuffer(in_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            if len(audio) == 0:
                continue

            # Default beam_size = 5
            segments, _ = model.transcribe(audio,
                                           beam_size=10,
                                           vad_filter=True,
                                           language=language,
                                           task="translate")
            text = "".join([seg.text for seg in segments]).strip()
            if text:
                print(">>>", text)

    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print("Stream error:", e)
    finally:
        process.stdout.close()
        process.stderr.close()
        process.wait()




