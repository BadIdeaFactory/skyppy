import youtube_dl

def get_video_id(url):
    ydl_opts = {
                "format": "bestaudio/best",
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            metadata = ydl.extract_info(url, download=False)["id"]

    return metadata

if __name__ == "__main__":
    assert get_video_id("https://www.youtube.com/watch?v=OG__SwkV3wg") == "OG__SwkV3wg"