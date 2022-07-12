from pyrogram.filters import command, me
from pyrogram.types import Message

from client import app


@app.on_message(me & command("stop", "!"))
async def stop(_, msg: Message) -> None:
    exit(1)
