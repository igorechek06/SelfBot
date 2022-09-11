import logging

from pyrogram.client import Client

from config import *

app = Client(
    session_name,
    api_id,
    api_hash,
    device_model="Python Self-Bot",
    system_version="trolling",
)
log = logging.getLogger()
logging.basicConfig(level=logging.WARNING)
