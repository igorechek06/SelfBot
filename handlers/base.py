from client import app
from pyrogram.filters import command, me
from pyrogram.types import Message


@app.on_message(me & command("stop", "!"))
async def stop(_, msg: Message) -> None:
    exit(1)
