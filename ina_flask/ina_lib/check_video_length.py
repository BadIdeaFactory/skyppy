import youtube_dl


class CheckVideoLength:
    """get video length in second without download"""

    def __init__(self):
        self.ydl_opts = {
            "format": "bestaudio/best",
        }

    def get(self, url: str) -> int:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            metadata = ydl.extract_info(url, download=False)
        return metadata["duration"]


if __name__ == "__main__":
    assert CheckVideoLength().get("https://www.youtube.com/watch?v=HS4ssEJk6qA") == 1657
    assert CheckVideoLength().get("https://www.youtube.com/watch?v=H0Srb7Qv4Qc") == 181
    assert CheckVideoLength().get("https://www.youtube.com/watch?v=OG__SwkV3wg") == 864
