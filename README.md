<h1 align="center">yt-dlp-bonus</h1>

<p align="center">
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/yt-dlp-bonus"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=MIT&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/yt-dlp-bonus"><img alt="PyPi" src="https://img.shields.io/pypi/v/yt-dlp-bonus"></a>
<a href="https://github.com/Simatwa/yt-dlp-bonus/releases"><img src="https://img.shields.io/github/v/release/Simatwa/yt-dlp-bonus?label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://pepy.tech/project/yt-dlp-bonus"><img src="https://static.pepy.tech/personalized-badge/yt-dlp-bonus?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/yt-dlp-bonus"/></a>
</p>
> A feature-rich command-line audio/video downloader bonus.

## Installation

```sh
pip install yt-dlp-bonus -U
```


## Usage

> [!WARNING]
> The package is at it's infancy stage.

### Download Video

```python
import logging
from yt_dlp_bonus import YoutubeDLBonus, Download

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

quality_formats = yt_bonus.get_videos_quality_by_extension(
    extracted_info=extracted_info
)

download = Download(yt=yt_bonus)
download.run(
    title=extracted_info.title, quality="480p", quality_infoFormat=quality_formats
)

```

### Download Audio

```python
import logging
from yt_dlp_bonus import YoutubeDLBonus, Download

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

video_url = "https://youtu.be/S3wsCRJVUyg"

yt_bonus = YoutubeDLBonus()

extracted_info = yt_bonus.extract_info_and_form_model(url=video_url)

quality_formats = yt_bonus.get_videos_quality_by_extension(
    extracted_info=extracted_info
)

download = Download(yt=yt_bonus)
download.run(
    title=extracted_info.title, quality="medium", quality_infoFormat=quality_formats
)

```

> [!NOTE]
> Incase requests are detected as coming from bot then consider using a proxy from **Canada** or any other country that will work. For more information on how to bypass bot detection then consider going through [this Wiki](https://github.com/yt-dlp/yt-dlp/wiki/Extractors).

# License

[The Unlicense](LICENSE)