from yt_dlp import YoutubeDL

def extract_video_metadata(url):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "activity_type": "video",
                "title": info.get("title"),
                "metadata": {
                    "author": info.get("uploader"),
                    "length_seconds": info.get("duration"),
                    "views": info.get("view_count"),
                    "publish_date": info.get("upload_date"),
                    "description": info.get("description")
                }
            }
    except Exception as e:
        return {"error": f"Failed to extract YouTube metadata: {str(e)}"}
