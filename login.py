from os import environ
from os.path import exists

from pyrogram.client import Client

while True:
    session_name = input("Client name -> ")
    if exists(f"{session_name}.session"):
        print("Client name is taken")
    else:
        break

client = Client(
    session_name,
    environ["apiId"],
    environ["apiHash"],
    device_model="Python Self-Bot",
    system_version="trolling",
)

with client:
    print("Done!")
    exit()
