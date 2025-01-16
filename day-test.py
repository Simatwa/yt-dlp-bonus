from yt_dlp_bonus import YoutubeDLBonus, Download

yt = YoutubeDLBonus()

extracted_info = yt.extract_info_and_form_model(
    "https://youtu.be/60ItHLz5WEA?si=waq9BdP3AW6p1QHv", process=False
)

down = Download(yt)

down.ydl_run_audio(extracted_info)
