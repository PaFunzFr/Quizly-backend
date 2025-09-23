# import json
# import yt_dlp

# URL = 'https://www.youtube.com/watch?v=rjE4XgsqyxE'

# ydl_opts = {
#     'format': 'm4a/bestaudio/best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }]
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     error_code = ydl.download(URL)

# ydl_opts = {
#     "format": "bestaudio/best",
#     "outtmpl": tmp_filename,
#     "quiet": True,
#     "noplaylist": True,
# }

import whisper

model = whisper.load_model("base")
result = model.transcribe("file.m4a")
print(result["text"])