"""Common and frequently required functions across the package"""

from typing import Sequence, Any
import subprocess
import logging
import re
from subprocess import CompletedProcess

logger = logging.getLogger(__file__)
"""yt-dlp-bonus logger"""

compiled_illegal_characters_pattern = re.compile(r"[^\w\-_\.\s()&|]")
"""Used to get rid of illegal characters in a filename"""

compiled_download_url_ip_pattern = re.compile(r"ip=[\w\W][^&]+")
"""Used for locating ip={ip} in download url"""


def assert_instance(obj, inst, name="Value"):
    """Asserts instanceship of an object"""
    assert isinstance(
        obj, inst
    ), f"{name} must be an instance of {inst} not {type(obj)}"


def assert_type(obj, type_: object | Sequence[object], name: str = "Value"):
    """Aserts obj is of type type_"""
    if isinstance(type_, Sequence):
        assert (
            type(obj) in type_
        ), f"{name} must be one of types {type_} not {type(obj)}"
    else:
        assert type(obj) is type_, f"{name} must be of type {type_} not {type(obj)}"


def assert_membership(elements: Sequence, member: Any, name="Value"):
    """Asserts member is one of the elements"""
    assert member in elements, f"{name} '{member}' is not one of {elements}"


def get_size_string(size_in_bytes: int) -> str:
    """Convert size from bytes to GB, MB and KB accordingly.

    Args:
        size_in_bytes (int)

    Returns:
        str: Size in Mb + "MB" string.
    """
    if isinstance(size_in_bytes, (int, float)):
        if size_in_bytes >= 1_000_000_000:
            size_in_gb = size_in_bytes / 1_000_000_000
            return str(round(size_in_gb, 2)) + " GB"
        elif size_in_bytes >= 1_000_000:
            size_in_mb = size_in_bytes / 1_000_000
            return str(round(size_in_mb, 2)) + " MB"
        else:
            size_in_kb = size_in_bytes / 1_000
            return str(round(size_in_kb, 2)) + " KB"
    else:
        return "[Unknown] Mb"


def run_system_command(command: str) -> tuple[bool, CompletedProcess | Exception]:
    """Execute command on system

    Args:
        command (str)

    Returns:
        tuple[bool, CompletedProcess| Exception]
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return (True, result)
    except subprocess.CalledProcessError as e:
        # Handle error if the command returns a non-zero exit code
        return (False, e)


def sanitize_filename(filename: str) -> str:
    """Remove illegal characters from a filename"""
    return re.sub(compiled_illegal_characters_pattern, "", filename)
