"""
path: config/config.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """"
    Settings class to load environment variables from .env file
    """
    BUCKET_NAME: str = os.getenv('BUCKET_NAME', "recombo-vision")
    BUCKET_FOLDER: str = os.getenv('BUCKET_FOLDER', "asi-cvs")
    CREDENTIALS: str = os.getenv('CREDENTIALS', "credentials.json")
    TEMPLATES_DIR: str = os.getenv('TEMPLATES_DIR', "templates")
    OUTPUT_DIR: str = os.getenv('OUTPUT_DIR', "output")
    PORT: int = os.getenv('PORT', 8000)
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', "ASI CV Generator")
    class Config:
        """
        Config class to load environment variables from .env file
        """
        env_file = ".env"

settings = Settings()
