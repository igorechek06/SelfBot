import typing
from tempfile import NamedTemporaryFile as tmp

from pyrogram.types import Message

from client import app


async def copy(
    msg: Message,
    chat_id: typing.Union[str, int],
    reply_to_message_id: typing.Optional[int] = None,
) -> Message:
    if msg.text:
        return await app.send_message(
            chat_id,
            text=msg.text,
            entities=msg.entities,
            disable_web_page_preview=not msg.web_page,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.photo:
        file = await download(msg, ".jpg")
        return await app.send_photo(
            photo=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.audio:
        file = await download(msg)
        return await app.send_audio(
            audio=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.document:
        file = await download(msg)
        return await app.send_document(
            document=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.video:
        file = await download(msg)
        return await app.send_video(
            video=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.animation:
        file = await download(msg)
        return await app.send_animation(
            animation=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.voice:
        file = await download(msg)
        return await app.send_voice(
            voice=file.name,
            caption=msg.caption,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.video_note:
        file = await download(msg)
        return await app.send_video_note(
            video_note=file.name,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.sticker:
        return await app.send_sticker(
            sticker=msg.sticker.file_id,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=msg.reply_markup,
        )
    elif msg.contact:
        return await app.send_contact(
            chat_id,
            phone_number=msg.contact.phone_number,
            first_name=msg.contact.first_name,
            last_name=msg.contact.last_name,
            vcard=msg.contact.vcard,
        )
    elif msg.location:
        return await app.send_location(
            chat_id,
            latitude=msg.location.latitude,
            longitude=msg.location.longitude,
        )
    elif msg.venue:
        return await app.send_venue(
            chat_id,
            latitude=msg.venue.location.latitude,
            longitude=msg.venue.location.longitude,
            title=msg.venue.title,
            address=msg.venue.address,
            foursquare_id=msg.venue.foursquare_id,
            foursquare_type=msg.venue.foursquare_type,
        )
    elif msg.poll:
        return await app.send_poll(
            chat_id,
            question=msg.poll.question,
            options=[opt.text for opt in msg.poll.options],
        )
    elif msg.game:
        return await app.send_game(
            chat_id,
            game_short_name=msg.game.short_name,
        )
    else:
        raise ValueError("Can't copy this message")


async def download(msg: Message, suffix: str = None) -> typing.IO:
    file = tmp("wb+", suffix=suffix)
    await msg.download(file.name)
    return file
