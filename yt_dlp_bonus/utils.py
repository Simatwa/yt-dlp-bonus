"""Common and frequently required functions across the package"""

from typing import Sequence, Any
import subprocess
import logging
from subprocess import CompletedProcess

logger = logging.getLogger(__file__)
"""yt-dlp-bonus logger"""


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
        assert type(obj) is type_, f"{name} must of type {type_} not {type(obj)}"


def assert_membership(elements: Sequence, member: Any):
    """Asserts member is one of the elements"""
    assert member in elements, f"{member} is not one of {elements}"


def get_size_in_mb_from_bytes(size_in_bytes: int) -> str:
    """Convert size in bytes to mb

    Args:
        size_in_bytes (int)

    Returns:
        str: Size in Mb + "MB" string.
    """
    if size_in_bytes:
        size_in_mb = size_in_bytes / 1_000_000
        return str(round(size_in_mb, 2)) + " MB"
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
