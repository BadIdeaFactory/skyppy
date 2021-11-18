import youtube_dl

def my_hook(d):
            if d["status"] == "finished":
                print("Done downloading, now converting ...")

class DownloadAudio:
    """get Audio download"""
    def __init__(self, output_file):
        self.filename = output_file 

        self.ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": self.filename,
                "noplaylist": True,
                "progress_hooks": [my_hook],
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
    def download(self, url: str) -> int:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.download([url])
        return result

if __name__ == "__main__":
    connection = DownloadAudio("./test/audio_test.mp3")
    print(connection.download("https://www.youtube.com/watch?v=S9ui5JK4c8k"))
