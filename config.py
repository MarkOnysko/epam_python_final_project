"""Module contains classes to store configurations"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Main configuration"""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "department_app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "arealybigsecret"


class TestConfig(Config):
    """Configuration for testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
