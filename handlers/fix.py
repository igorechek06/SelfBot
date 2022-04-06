from pyrogram.filters import forwarded, me
from pyrogram.types import Message

from client import app


@app.on_message(me & forwarded)
async def forward(_, msg: Message) -> None:
    m = await app.get_messages(msg.chat.id, msg.message_id - 1)
    if (
        m.forward_date is None
        and m.from_user.id == msg.from_user.id
        and m.date + 1 >= msg.date
    ):
        await m.copy(msg.chat.id, reply_to_message_id=msg.message_id)
        await m.delete()
