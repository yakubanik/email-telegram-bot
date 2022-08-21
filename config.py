""" Настройки проекта. """

import os
from pathlib import Path

HOST = "smtp.gmail.com"
PORT = 587
DOWNLOAD_PATH = Path('attachments')
TOKEN = os.getenv('TOKEN')
MY_ID = os.getenv('MY_ID')
SENDER = os.getenv('SENDER')
RECEIVER = os.getenv('RECEIVER')
PASSWORD = os.getenv('PASSWORD')
