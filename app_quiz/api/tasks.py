import os
import re
import yt_dlp
import whisper
from google import genai
from google.genai import types
from decouple import config

prompt = """Based on the following transcript, generate a quiz in valid JSON format.

The quiz must follow this exact structure:

{{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
  "questions": [
    {{
      "question_title": "The question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    }},
    ...
    (exactly 10 questions)
  ]
}}

Requirements:
- Each question must have exactly 4 distinct options.
- Only one correct answer, present in options.
- Output ONLY the JSON, no additional text, explanations, or formatting.
- The output MUST be a valid JSON parsable with standard JSON parsers.
"""

API_KEY = config('GEMINI_API_KEY')

client = genai.Client(
    api_key= API_KEY,
    http_options=types.HttpOptions(api_version='v1alpha')
)

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

            model = whisper.load_model("tiny")
            result = model.transcribe(audio_filename)
            transcript = result["text"]

    finally:
        # delete audiofile after transcription
        if audio_filename and os.path.exists(audio_filename):
            os.remove(audio_filename)
    
    return transcript


def clean_json(text: str) -> str:
    return re.sub(r"^```(?:json)?|```$", "", text, flags=re.DOTALL).strip()


def generateQuiz(transcript):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=[prompt, transcript]
    )
    quiz_raw = response.candidates[0].content.parts[0].text
    quiz = clean_json(quiz_raw)
    
    return quiz