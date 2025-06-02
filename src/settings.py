class Settings():
    is_dragging_over = False
    is_dragging_volume = False
    is_playing = False
    fft_window_size = 4096

    download_audio_qualities = {
        'high-quality': 'bestaudio/best',
        'low-quality': 'worstaudio/worst'
    }

    download_audio_quality  = download_audio_qualities['high-quality']

    download_audio_bitrate = 192

    download_audio_ext = 'mp3'
    download_output_dir = 'audio'