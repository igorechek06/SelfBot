from pyrogram import StopPropagation
from pyrogram.types import Message


async def throw(text: str, msg: Message, condition: bool = False, type: str = "ERROR"):
    if not condition:
        edit = msg.edit_caption if msg.caption is not None else msg.edit_text
        msg_text = msg.text or msg.caption

        await edit(f"<code>{msg_text}</code>\n\n{type}: {text}", parse_mode="html")
        raise StopPropagation()
