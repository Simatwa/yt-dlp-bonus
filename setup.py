from setuptools import setup


setup(
    name="yt-dlp-bonus",
    version="0.1.5",
    license="The Unlicense",
    author="Smartwa",
    maintainer="Smartwa",
    author_email="simatwacaleb@proton.me",
    description="An extension of yt-dlp targeting YouTube with pydantic support.",
    packages=["yt_dlp_bonus"],
    url="https://github.com/Simatwa/yt-dlp-bonus",
    project_urls={
        "Bug Report": "https://github.com/Simatwa/yt-dlp-bonus/issues/new",
        "Homepage": "https://github.com/Simatwa/yt-dlp-bonus",
        "Source Code": "https://github.com/Simatwa/yt-dlp-bonus",
        "Issue Tracker": "https://github.com/Simatwa/yt-dlp-bonus/issues",
        "Download": "https://github.com/Simatwa/yt-dlp-bonus/releases",
        "Documentation": "https://github.com/Simatwa/yt-dlp-bonus/",
    },
    entry_points={
        "console_scripts": [],
    },
    install_requires=["yt-dlp>=2024.12.13", "pydantic==2.9.2"],
    python_requires=">=3.10",
    keywords=[
        "yt-dlp",
        "yt-dlp-bonus",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Intended Audience :: Developers",
        "License :: Free For Home Use",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
