import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'uploads'))
    MAX_CONTENT_LENGTH = 20480 * 1024  # 20 MB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    LANGUAGES = ['en', 'fi']
    USER_CREATION_SECRET = os.environ.get('USER_CREATION_SECRET') or 'a-secret-key-for-user-creation'