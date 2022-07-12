import logging

from config import *
from pyrogram.client import Client

app = Client(
    session_name,
    api_id,
    api_hash,
    device_model="Python Self-Bot",
    system_version="trolling",
)
log = logging.getLogger()
logging.basicConfig(level=logging.WARNING)

__all__ = ["app"]
