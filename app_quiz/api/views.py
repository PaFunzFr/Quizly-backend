from rest_framework import views, status
from rest_framework.response import Response

from .serializers import QuizCreateSerializer

import json
import yt_dlp


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

def download(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)


class QuizCreateView(views.APIView):
    serializer_class = QuizCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['video_url']
            download(url)

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


