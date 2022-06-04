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


def get_youtube_id_from_request(request) -> dict:
    posted = {}
    posted["link_video"] = "https://" + request.args.get("url", default="*", type=str)
    id_youtube_file = (
        request.args.get("url", default="*", type=str).split("?v=")[1] + ".json"
    )
    id_youtube = request.args.get("url", default="*", type=str).split("?v=")[1]
    posted["id_youtube"] = id_youtube
    posted["id_youtube_file"] = id_youtube_file
    return posted
