# what to install
FROM python:3.11-slim

# install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# install folder of image
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yt-dlp
RUN yt-dlp -U
RUN python -c "import whisper; whisper.load_model('tiny')"

# copy all
COPY . . 

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 