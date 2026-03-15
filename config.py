import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = os.urandom(32).hex()  # для локального теста

    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Render иногда даёт postgres:// вместо postgresql://
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
