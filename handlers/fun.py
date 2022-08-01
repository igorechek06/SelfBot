from asyncio import sleep
from re import compile
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile as tmp

from pyrogram.filters import (
    animation,
    audio,
    command,
    document,
    me,
    private,
    reply,
    video,
)
from pyrogram.types import Message

from client import app
from libs.errors import throw
from libs.util import download

WIN_MAP = {
    "🎲": [6],
    "🎯": [6],
    "🎳": [6],
    "🏀": [4, 5],
    "⚽": [4, 5],
    "🎰": [1, 22, 43, 64],
}
SPAM = compile(r"\{(?P<code>[^{}]+)\}")


@app.on_message(me & command("words", "!"))
async def words(_, msg: Message) -> None:
    args = msg.command[1:]
    await throw("Too few arguments ({delay} {message})", msg, len(args) >= 2)
    try:
        delay = float(args[0])
        text = args[1:]
    except Exception:
        await throw("Incorrect arguments", msg)
    await throw("Text is too big (max 75 words)", msg, len(text) <= 75)

    for i in range(len(text)):
        await msg.edit_text(" ".join(text[: i + 1]))
        await sleep(delay)


@app.on_message(me & command("chars", "!"))
async def chars(_, msg: Message) -> None:
    args = msg.command[1:]
    await throw("Too few arguments ({delay} {message})", msg, len(args) >= 2)
    try:
        delay = float(args[0])
        text = " ".join(args[1:])
    except Exception:
        await throw("Incorrect arguments", msg)
    await throw("Text is too big (max 75 chars)", msg, len(text) <= 75)

    for i in range(len(text)):
        if text[i] == " ":
            continue
        await msg.edit_text(text[: i + 1])
        await sleep(delay)


@app.on_message(me & command("spam", "!"))
async def spam(_, msg: Message) -> None:
    args = msg.command[1:]
    rid = msg.reply_to_message.message_id if msg.reply_to_message is not None else None
    await throw("Too few arguments ({delay} {count} {f_message})", msg, len(args) >= 3)
    try:
        delay = float(args[0])
        count = int(args[1])
        text = " ".join(args[2:])
        code = [m.group("code") for m in SPAM.finditer(text)]
        text = SPAM.sub("{}", text)
    except:
        await throw("Incorrect arguments", msg)

    await msg.delete()
    try:
        for i in range(count):
            await msg.reply_text(
                text.format(*[eval(c, {"i": i}, {}) for c in code]),
                quote=False,
                reply_to_message_id=rid,
            )
            await sleep(delay)
    except:
        pass


@app.on_message(me & command("plan", "!"))
async def plan(_, msg: Message) -> None:
    args = msg.command[1:]
    rid = msg.reply_to_message.message_id if msg.reply_to_message is not None else None
    await throw("Too few arguments ({delay} {count} {f_message})", msg, len(args) >= 3)
    try:
        delay = int(args[0])
        count = int(args[1])
        text = " ".join(args[2:])
        code = [m.group("code") for m in SPAM.finditer(text)]
        text = SPAM.sub("{}", text)
    except:
        await throw("Incorrect arguments", msg)

    await msg.delete()
    date = msg.date + delay
    try:
        for i in range(count):
            await msg.reply_text(
                text.format(*[eval(c, {"i": i}, {}) for c in code]),
                quote=False,
                reply_to_message_id=rid,
                schedule_date=date + i * delay,
            )
    except:
        pass


@app.on_message(me & ~private & command("dice", "!"))
async def dice(_, msg: Message):
    args = msg.command[1:]
    await throw("Too few arguments ({count} {dice} {value})", msg, len(args) >= 3)
    try:
        count = int(args[0])
        dice = args[1]
        if args[2].lower() == "win":
            value = WIN_MAP[dice]
        else:
            value = [int(args[2])]
    except Exception:
        await throw("Incorrect arguments", msg)
    await throw("Dice incorrect (🎲,🎯,🎳,🏀,⚽,🎰 only)", msg, dice in WIN_MAP)
    if dice in ["🎲", "🎯", "🎳"]:
        await throw(
            "🎲,🎯,🎳 can have values from 1 to 6",
            msg,
            all([v in range(1, 7) for v in value]),
        )
    elif dice in ["🏀", "⚽"]:
        await throw(
            "🏀,⚽ can have values from 1 to 5",
            msg,
            all([v in range(1, 6) for v in value]),
        )
    else:  # dice == "🎰"
        await throw(
            "🎰 can have values from 1 to 64",
            msg,
            all([v in range(1, 65) for v in value]),
        )

    await msg.delete()
    for _ in range(count):
        try:
            while True:
                m = await app.send_dice(msg.chat.id, dice, True)
                print(m.dice.value, value, m.dice.value in value)
                if m.dice.value in value:
                    break
                else:
                    await m.delete()
        except Exception:
            pass


@app.on_message(me & audio & command("voice", "!"))
async def voice(_, msg: Message) -> None:
    await msg.delete()
    file = await download(msg)
    await msg.download(file.name)
    await msg.reply_voice(file.name, quote=False)


@app.on_message(me & (video | animation) & command("note", "!"))
async def note(_, msg: Message) -> None:
    await msg.delete()

    inp = msg.animation or msg.video
    size = min(max(inp.height, inp.width), 512)

    inp_file = await download(msg)
    with tmp("w+b", suffix=".mp4") as out_file:
        run(
            f"ffmpeg -y -i {inp_file.name} -vf scale={size}:{size},setsar=1:1 {out_file.name}",
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        await msg.reply_video_note(out_file.name, quote=False)
