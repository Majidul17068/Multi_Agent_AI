import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Vector DB Configuration
VECTOR_DB_DIR = "data/vectordb"

# Search Configuration
DEFAULT_NEWS_COUNT = 5
SEARCH_ENGINE_URL = "https://www.google.com/search"
NEWS_SOURCES = [
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "cnn.com",
    "theguardian.com"
]

# Translation Configuration
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "bn": "Bengali"
}
