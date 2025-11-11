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

RUN mkdir -p /usr/src/app/staticfiles && \
    chown -R www-data:www-data /usr/src/app/staticfiles

EXPOSE 8001

# run migrations, collectstatic and start gunicorn as www-data
USER www-data
CMD sh -c "python manage.py migrate --noinput && \
            python manage.py collectstatic --noinput && \
            gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 3 --threads 2  --timeout 1800"