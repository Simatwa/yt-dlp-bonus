"""
A minimal yet handy extended version of yt-dlp with focus on
providing pydantic support to YoutubeDL.

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
import logging
from yt_dlp_bonus import YoutubeDLBonus, Download

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

quality_formats = yt_bonus.get_video_qualities_with_extension(
    extracted_info=extracted_info
)

download = Download(yt=yt_bonus)
download.run(
    title=extracted_info.title, quality="480p", quality_infoFormat=quality_formats
)

```

## Download Audio

```python
import logging
from yt_dlp_bonus import YoutubeDLBonus, Download

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

quality_formats = yt_bonus.get_video_qualities_with_extension(
    extracted_info=extracted_info
)

download = Download(yt=yt_bonus)
download.run(
    title=extracted_info.title, quality="medium", quality_infoFormat=quality_formats
)
```
"""

from importlib import metadata
from yt_dlp_bonus.main import YoutubeDLBonus, Download, PostDownload

try:
    __version__ = metadata.version("yt-dlp-bonus")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/yt-dlp-bonus"

__all__ = ["YoutubeDLBonus", "Download", "PostDownload"]
