from jp_live_transcript import get_youtube_livestream_url, get_recording_and_transrecord

if __name__ == '__main__':
    youtube_url = "https://www.youtube.com/watch?v=usc2l-pue9Y&embeds_referring_euri=https%3A%2F%2Fholodex.net%2F&embeds_referring_origin=https%3A%2F%2Fholodex.net&source_ve_path=MjM4NTE"

    yt_audio_link = get_youtube_livestream_url(youtube_url)

    get_recording_and_transrecord(yt_audio_link, "ja")
