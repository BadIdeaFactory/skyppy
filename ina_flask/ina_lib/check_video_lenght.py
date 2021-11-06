import youtube_dl

class CheckVideoLenght:
    """get video lenght in second without download"""
    def __init__(self):
        self.ydl_opts = {
                "format": "bestaudio/best",
            }

    def get(self, url: str) -> int:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            metadata = ydl.extract_info(url, download=False)
        return metadata['duration']

if __name__ == "__main__":
    assert CheckVideoLenght().get( "https://www.youtube.com/watch?v=HS4ssEJk6qA") == 1657
    assert CheckVideoLenght().get( "https://www.youtube.com/watch?v=H0Srb7Qv4Qc") == 181
    assert CheckVideoLenght().get( "https://www.youtube.com/watch?v=OG__SwkV3wg") == 864