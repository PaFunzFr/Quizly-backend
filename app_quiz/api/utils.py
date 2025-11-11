import os
import re
import yt_dlp
import whisper
from google import genai
from google.genai import types
from decouple import config

cookies_path = os.getenv("YTDLP_COOKIES_PATH", "/usr/src/app/cookies.txt")

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

# set media folder for yt temp files (/media/temp/)
media_root = os.path.join(os.getcwd(), "media", "temp")

useragent = os.getenv("YTDLP_UA", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    "quiet": True,
    "noplaylist": True,
    'outtmpl': os.path.join(media_root,'%(id)s.%(ext)s'), # save file as "VIDEO_ID.m4a"
    'progress_hooks': [],
    'http_headers': {
        'User-Agent': useragent,
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept': '*/*',
        'Referer': 'https://www.youtube.com/',
    },
}


def download_and_transcribe(url):
    """
    Download audio from a YouTube video and transcribe it to text.

    This function:
    - Downloads the audio from the provided YouTube URL into a temporary folder.
    - Uses the Whisper 'tiny' model to transcribe the audio into text.
    - Deletes the temporary audio file after transcription.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The transcribed text from the video audio.

    Raises:
        yt_dlp.utils.DownloadError: If the video cannot be downloaded.
        whisper.WhisperError: If transcription fails.
    """

    # create folder if not existing
    os.makedirs(media_root, exist_ok=True)
    
    audio_filename = None
    transcript = ""

    if not config('DEBUG'):
        ydl_opts["cookies"] = cookies_path
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True) #raises yt_dlp.utils.DownloadError
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
    """
    Clean a string containing JSON code blocks.

    Removes Markdown-style code fences (``` or ```json) and trims whitespace.

    Args:
        text (str): The raw JSON string possibly wrapped in code fences.

    Returns:
        str: Cleaned JSON string ready for parsing.
    """
    return re.sub(r"^```(?:json)?|```$", "", text, flags=re.DOTALL).strip()


def generateQuiz(transcript):
    """
    Generate a quiz in JSON format from a transcript using the Gemini AI model.

    This function:
    - Sends the transcript and a predefined prompt to the Gemini model.
    - Receives a raw quiz output from the AI.
    - Cleans the output to ensure it is valid JSON.

    Args:
        transcript (str): The text transcript from which to generate the quiz.

    Returns:
        str: A JSON-formatted string representing the quiz, containing
            title, description, and exactly 10 questions with options and answers.

    Raises:
        genai.Error: If content generation fails.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite', #'gemini-2.0-flash-001',
        contents=[prompt, transcript]
    )
    quiz_raw = response.candidates[0].content.parts[0].text
    quiz = clean_json(quiz_raw)
    
    return quiz