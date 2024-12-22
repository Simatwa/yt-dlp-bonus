class UserInputError(Exception):
    """Raised when user entered incorrect values"""


class FileSizeOutOfRange(Exception):
    """Raised when a file to be downloaded is not within the min_filesize and max_filesize"""


class UknownDownloadFailure(Exception):
    """Raised when ytdl fails to download a file due to unknown reasons."""
