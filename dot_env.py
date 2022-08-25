# dot_env.py
import os
from dotenv import load_dotenv

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN', '')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 0)

load_dotenv(override=True)
