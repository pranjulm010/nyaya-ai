import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# API Keys
# ==========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
KANOON_API_KEY = os.getenv("KANOON_API_KEY", "")

# ==========================
# Models
# ==========================
CHEAP_MODEL = os.getenv("CHEAP_MODEL", "llama-3.1-8b-instant")
MEDIUM_MODEL = os.getenv("MEDIUM_MODEL", "llama-3.3-70b-versatile")
PREMIUM_MODEL = os.getenv("PREMIUM_MODEL", "llama-3.3-70b-versatile")

DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0"))

# ==========================
# Storage
# ==========================
CHROMA_DIR = os.getenv(
    "CHROMA_DIR",
    str(BASE_DIR / "storage" / "vector_db")
)

DOCUMENT_UPLOAD_DIR = os.getenv(
    "DOCUMENT_UPLOAD_DIR",
    str(BASE_DIR / "storage" / "uploaded_pdfs")
)

# ==========================
# Limits
# ==========================
MAX_FREE_QUERIES = int(os.getenv("MAX_FREE_QUERIES", "10"))
MAX_PUBLIC_QUERIES = int(os.getenv("MAX_PUBLIC_QUERIES", "100"))
MAX_LAWYER_QUERIES = int(os.getenv("MAX_LAWYER_QUERIES", "1000"))

MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))

# ==========================
# App
# ==========================
DEBUG = os.getenv("DEBUG", "True") == "True"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")