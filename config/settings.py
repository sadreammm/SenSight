import os
import dotenv

dotenv.load_dotenv()

class Settings:
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    HOST = "127.0.0.1"
    PORT = 8000

settings = Settings()