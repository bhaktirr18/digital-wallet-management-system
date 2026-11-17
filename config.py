
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///wallet.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF protection
    WTF_CSRF_ENABLED = True

    # Debug mode
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
