from importlib import metadata
import logging

try:
    __version__ = metadata.version("yt-dlp-bonus")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/yt-dlp-bonus"


logger = logging.getLogger(__file__)
"""yt-dlp-bonus logger"""
