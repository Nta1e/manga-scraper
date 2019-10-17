from os import getenv
from dotenv import load_dotenv
from .base import *

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv("DB_NAME", "manga_db"),
        'USER': getenv("DB_USER", "postgres"),
        'PASSWORD': getenv("DB_PASSWORD", "password"),
        'port': getenv("DB_PORT", '5432')
    }
}
