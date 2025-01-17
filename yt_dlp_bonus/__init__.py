"""
A minimal yet handy extended version of yt-dlp with focus on
providing pydantic support to YoutubeDL extracts.

## Search Videos

```python
from yt_dlp_bonus import YoutubeDLBonus

yt = YoutubeDLBonus()

search_results = yt.search_and_form_model(
    query="hello",
    limit=1
    )

print(search_results)
```

## Download Video

```python
from yt_dlp_bonus import YoutubeDLBonus, Downloader

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

downloader = Downloader(yt=yt_bonus)
downloader.ydl_run(
    extracted_info, video_format="bestvideo"
)

```

## Download Audio

```python
from yt_dlp_bonus import YoutubeDLBonus, Downloader

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

downloader = Downloader(yt=yt_bonus)

downloader.ydl_run(
    extracted_info, video_format=None, audio_format="bestaudio"
)
```
"""

from importlib import metadata
from yt_dlp_bonus.main import YoutubeDLBonus, Downloader, PostDownload

try:
    __version__ = metadata.version("yt-dlp-bonus")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/yt-dlp-bonus"

__all__ = ["YoutubeDLBonus", "Downloader", "PostDownload"]
