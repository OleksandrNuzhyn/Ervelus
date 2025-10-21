from dotenv import load_dotenv # TODO: Remove
import os
from pathlib import Path

load_dotenv() # TODO: Remove

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS = [
    'generations',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Trueelse23#',
        'HOST': '34.116.178.6',
        'PORT': '5432'
    }
}

STORAGE_BUCKET_NAME = os.getenv("GCP_STORAGE_BUCKET_NAME")