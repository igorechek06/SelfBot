from pyrogram.filters import command, create, forwarded, me, private, reply, text
from pyrogram.types import Message

from client import app
from config import save_settigns, settings
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


@app.on_message(me & command("backup", "!") & private)
async def set_backup(_, msg: Message) -> None:
    if msg.chat.id not in settings["backup"]:
        await msg.edit_text("You have been added as a backup account")
        settings["backup"].append(msg.chat.id)
    else:
        await msg.edit_text("You have been removed as a backup account")
        settings["backup"].remove(msg.chat.id)
    save_settigns()


@app.on_message(me & command("backups", "!"))
async def backup_list(_, msg: Message) -> None:
    if settings["backup"] != []:
        t = "Backup list:\n"
        for id in settings["backup"]:
            t += f' - <a href="tg://user?id={id}">{id}</a>\n'
        await msg.edit_text(t, parse_mode="HTML")
    else:
        await msg.edit_text("Backup list is empty")


@app.on_message(text & ~me & create(lambda _, __, m: m.chat.id == 777000))
async def backup_and_private(_, msg: Message) -> None:
    # Private
    await msg.reply(f"Telegram:\n<spoiler>{msg.text}</spoiler>", parse_mode="HTML")
    await msg.delete()

    # Backup
    for id in settings["backup"]:
        await app.send_message(
            id,
            f"Telegram:\n<spoiler>{msg.text}</spoiler>",
            parse_mode="HTML",
        )
