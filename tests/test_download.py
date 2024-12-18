import pytest
from yt_dlp_bonus.main import Download


@pytest.fixture
def download():
    return Download()
