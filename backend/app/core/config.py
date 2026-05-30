"""
Configuration settings for EduTutor BD
All values loaded from Vercel Environment Variables
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Groq AI (replaces Gemini for generation)
    GROQ_API_KEY: str = ""

    # Google Gemini (for embeddings only)
    GEMINI_API_KEY: str = ""

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # ChromaDB path (relative, included in repo)
    CHROMA_DB_PATH: str = "./data/chroma_db"
    CHROMA_COLLECTION: str = "nctb_textbooks"

    # JWT (kept for compatibility)
    SECRET_KEY: str = "change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"

settings = Settings()
