import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

WORK_DIR = pathlib.Path().cwd().resolve()

STATIC_DIR = os.getenv('STATIC_DIR', 'static')
STATIC_PATH = WORK_DIR / STATIC_DIR

MEDIA_DIR = os.getenv('MEDIA_DIR', 'images')
MEDIA_PATH = WORK_DIR / MEDIA_DIR