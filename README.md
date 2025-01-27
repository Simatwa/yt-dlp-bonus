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

This library does a simple yet the Lord's work; extends [yt-dlp](https://github.com/yt-dlp/yt-dlp) *(YoutubeDL)* and adds modelling support to the extracted YoutubeDL results using [pydantic](https://github.com/pydantic/pydantic).

## Installation

```sh
pip install yt-dlp-bonus -U
```

## Usage

<details open>

<summary>

### Search videos

</summary>

```python
from yt_dlp_bonus import YoutubeDLBonus

yt = YoutubeDLBonus()

search_results = yt.search_and_form_model(
    query="hello",
    limit=1
    )

print(search_results)

```

</details>

<details>

<summary>

### Download Video

</summary>

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

</details>

<details>
<summary>

### Download Audio

</summary>

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

</details>

## CLI

### Download Video

Usage : `$ yt-dlpb download-video <VIDEO-URL>`

<details>

<summary>
<code>$ python -m yt_dlp_bonus download-video --help</code>
</summary>

```
                                                                                
 Usage: python -m yt_dlp_bonus download-video [OPTIONS] URL                     
                                                                                
 Download a youtube video                                                       
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    url      TEXT  Link pointing to a Youtube video [default: None]         │
│                     [required]                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --quality                        [144p|240p|360p|480p  Video quality to      │
│                                  |720p|1080p|2k|4k|8k  download              │
│                                  |best]                [default: best]       │
│ --dir                            DIRECTORY             Directory to save the │
│                                                        video to              │
│                                                        [default:             │
│                                                        /home/smartwa/git/sm… │
│ --format                         [webm|mp4]            Video format to       │
│                                                        process ie. mp4 or    │
│                                                        webm                  │
│                                                        [default: webm]       │
│ --quiet            --no-quiet                          Do not stdout         │
│                                                        anything              │
│                                                        [default: no-quiet]   │
│ --subtitle-lang                  TEXT                  Subtitle language to  │
│                                                        embed in the video    │
│                                                        [default: None]       │
│ --help                                                 Show this message and │
│                                                        exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯


```

</details>

### Download Audio

Usage : `$ yt-dlp download-audio <VIDEO-URL>`

<details>
<summary>
<code>$ python -m yt_dlp_bonus download-audio --help</code>
</summary>

```
                                                                                
 Usage: python -m yt_dlp_bonus download-audio [OPTIONS] URL                     
                                                                                
 Download audio version of a YouTube video                                      
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    url      TEXT  Link pointing to a Youtube video [default: None]         │
│                     [required]                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --quality                  [ultralow|low|medium|be  Video quality to         │
│                            staudio]                 download                 │
│                                                     [default: bestaudio]     │
│ --dir                      DIRECTORY                Directory to save the    │
│                                                     video to                 │
│                                                     [default:                │
│                                                     /home/smartwa/git/smart… │
│ --format                   [webm|mp4]               Video format to process  │
│                                                     ie. mp4 or webm          │
│                                                     [default: webm]          │
│ --bitrate                  [64k|96k|128k|192k|256k  Audio bitrate while      │
│                            |320k]                   converting to mp3        │
│                                                     [default: None]          │
│ --quiet      --no-quiet                             Do not stdout anything   │
│                                                     [default: no-quiet]      │
│ --help                                              Show this message and    │
│                                                     exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯

```

</details>

<details>

<summary>
<code>$ python -m yt_dlp_bonus --help</code>
</summary>

```
                                                                                
 Usage: python -m yt_dlp_bonus [OPTIONS] COMMAND [ARGS]...                      
                                                                                
 Download Youtube videos in a number of formats.                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ download-video   Download a youtube video                                    │
│ download-audio   Download audio version of a YouTube video                   │
╰──────────────────────────────────────────────────────────────────────────────╯


```

</details>

> [!NOTE]
> Incase requests are detected as coming from bot then consider using a proxy from **Canada**, **USA** or any other location that will work. For more information on how to bypass bot detection then consider going through [this Wiki](https://github.com/yt-dlp/yt-dlp/wiki/Extractors).

# License

[The Unlicense](LICENSE)
