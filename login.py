from os.path import exists

from pyrogram.client import Client

from config import api_hash, api_id

while True:
    session_name = input("Client name -> ")
    if exists(f"{session_name}.session"):
        print("Client name is taken")
    else:
        break

client = Client(
    session_name,
    api_id,
    api_hash,
    device_model="Python Self-Bot",
    system_version="trolling",
)

with client:
    print("Done!")
    exit()
