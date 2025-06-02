import yt_dlp
import os
from settings import Settings

class YoutubeHandler():
    def __init__(self):
        self.output_dir = os.path.join(os.getcwd(), Settings.download_output_dir)

    def get_audio_from_youtube(self, video_url: str) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        ydl_opts = {
            "format": Settings.download_audio_quality,
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": Settings.download_audio_ext,
                "preferredquality": Settings.download_audio_bitrate,
            }],
            "keepvideo": False,
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get("title", "audio")

        for file in os.listdir(self.output_dir):
            if file.endswith('.' + Settings.download_audio_ext) and title in file:
                return os.path.join(self.output_dir, file)