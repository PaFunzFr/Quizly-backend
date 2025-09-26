# Backend Project Quizly - a freelance developer platform

This is the backend for a Django REST API application.  
The project is based on Django and Django REST Framework and uses a classic app structure (e.g. app_auth, ...).  
With this API you can create Quizes from Youtube Video URLs.

### Features

- **User Authentication**: Register, login, and logout functionality
- **Quiz Generation**: Create quizzes from Youtube-URLs
- **Quiz Taking**: Interactive quiz interface with multiple-choice questions
- **Results Review**: View quiz results with correct/incorrect answers
- **Quiz Management**: View, edit, and delete quizzes

---

## Project Structure

```
backend-quizly/
│
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── app_auth/
│   ├── __init__.py
│   ├── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── tests/
│       ├── __init__.py
│       ├── test_login.py
│       ├── test_cookies.py
│       └── test_register.py
│
├── app_quiz/
│   ├── __init__.py
│   ├── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── permissions.py
│   │   ├── urls.py
│   │   └── utils.py
│   └── tests/
│       ├── __init__.py
│       ├── test_quizCreate.py
│       └── test_quizzes.py
│
├── media/
│   └── temp/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── conftest.py                        # falls du ALLE Fixtures zentral hier halten willst (alternativ im tests/)
├── pytest.ini
└── .env
```

---

## Environment Setup

Create a .env file in the root folder with the following variables:

```
SECRET_KEY=' placeholder'
DEBUG= True / False
GEMINI_API_KEY= 'placeholder'
```

Make sure to replace placeholders with your actual keys.

---

## Requirements

- Python 3.13+
- FFmpeg (für yt-dlp/Whisper)

- Core dependencies:
    - Django 5, Django REST Framework, SimpleJWT
    - django-cors-headers, drf-spectacular
    - yt-dlp, openai-whisper/ctranslate2/onnxruntime (ASR)
    - google-genai (Quiz-Generierung)

full list: requirements.txt (Installation guide see below)

---

## Install Dependencies

All required Python packages are listed in requirements.txt.
They include Django, DRF, JWT authentication, DRF Spectacular (Swagger/OpenAPI),
Whisper for transcription, yt-dlp for YouTube downloads, and Google Gemini API client for quiz generation.

```
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Docker Setup

Build Docker Image

```docker build -tag coderr-backend .```

This will also pre-load the Whisper tiny model.

---

## Run Using Docker Compose

```docker-compose up --build```

The backend will be exposed on http://localhost:8000.
Source code is mounted to /usr/src/app for live updates.

---

## Manual Run (without Docker)

```
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

```
pip install --upgrade pip
pip install -r requirements.txt
```

```
python manage.py migrate
python manage.py runserver
```

---

## Database

The project uses SQLite by default for local development.

Database file will be created automatically in the project root after migration.

```
pathon manage.py makemigrations
python manage.py migrate
```

---

## Running Tests

Tests are written using pytest and pytest-django.

# Run all tests
```
pytest
```

# Run with coverage report
```
pytest --cov=.`
``

The test fixtures use pre-created users, JWT tokens, and dummy quizzes. Make sure your .env is properly set up before running tests.

---

## API Documentation

Swagger/OpenAPI documentation is automatically generated using drf-spectacular.

Once the server is running, you can access it at:

http://localhost:8000/schema/
http://localhost:8000/swagger/
http://localhost:8000/redoc/

---

## License

MIT License – see [LICENSE](LICENSE)  
