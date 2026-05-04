import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

WORK_DIR = pathlib.Path().cwd().resolve()

STATIC_DIR = os.getenv('STATIC_DIR', 'static')
STATIC_PATH = WORK_DIR / STATIC_DIR

MEDIA_DIR = os.getenv('MEDIA_DIR', 'images')
MEDIA_PATH = WORK_DIR / MEDIA_DIR

LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_PATH = WORK_DIR / LOG_DIR

IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

