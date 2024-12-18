"""
A minimal yet handy extended version of yt-dlp with focus on
fast and easy download of Youtube videos.
"""

import logging
from importlib import metadata
from yt_dlp_bonus.main import YoutubeDLBonus, Download, PostDownload

try:
    __version__ = metadata.version("yt-dlp-bonus")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/yt-dlp-bonus"


logger = logging.getLogger(__file__)
"""yt-dlp-bonus logger"""

__all__ = ["YoutubeDLBonus", "Download", "PostDownload"]
