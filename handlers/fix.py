from pyrogram.filters import command, forwarded, me, reply
from pyrogram.types import Message

from client import app
from libs.errors import throw
from libs.util import copy


@app.on_message(me & forwarded)
async def forward(_, msg: Message) -> None:
    m = await app.get_messages(msg.chat.id, msg.message_id - 1)

    if m.empty:
        return

    if (
        m.forward_date is None
        and (m.chat.type == "channel" or m.from_user.id == msg.from_user.id)
        and m.date + 1 >= msg.date
    ):
        await m.copy(msg.chat.id, reply_to_message_id=msg.message_id)
        await m.delete()


@app.on_message(me & command("steal", "!"))
async def steal(_, msg: Message) -> None:
    args = msg.command[1:]
    await throw("Too few arguments ({message_link})", msg, len(args) >= 1)
    try:
        link = args[0].split("/")
        c_id, m_id = link[-2:]
        if link[3] == "c":
            m_id = int(m_id)
            c_id = int(f"-100{c_id}")
        else:
            m_id = int(m_id)
            c_id = str(c_id)
    except Exception:
        await throw("Incorrect arguments", msg)

    await msg.delete()
    m = await app.get_messages(c_id, m_id)
    await copy(m, msg.chat.id, msg.reply_to_message_id)


@app.on_message(me & command("save", "!") & reply)
async def save(_, msg: Message) -> None:
    await msg.delete()
    await copy(msg.reply_to_message, "self")
