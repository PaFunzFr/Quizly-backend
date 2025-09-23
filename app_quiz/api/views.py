from rest_framework import views, status
from rest_framework.response import Response

from .serializers import QuizCreateSerializer

import json
import os
import yt_dlp
import whisper


ydl_opts = {
    'format': 'm4a/bestaudio/best',
    "quiet": True,
    "noplaylist": True,
    'outtmpl': '%(id)s.%(ext)s' # save file as "VIDEO_ID.m4a"
    # 'postprocessors': [{  # Extract audio using ffmpeg
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'm4a',
    # }]
}





def download_and_transcribe(url):
    audio_filename = None
    transcript = ""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_filename = ydl.prepare_filename(info)

            model = whisper.load_model("base")
            result = model.transcribe(audio_filename)
            transcript = result["text"]
            #print(result["text"])

    finally:
        # delete audiofile after transcription
        if audio_filename and os.path.exists(audio_filename):
            os.remove(audio_filename)
    
    return transcript

class QuizCreateView(views.APIView):
    serializer_class = QuizCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['video_url']
            transcript_text = download_and_transcribe(url)

            return Response({"transcript": transcript_text}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


