from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import STREAM_MODE, URL, LOG_CHANNEL
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    if STREAM_MODE == False:
        return 
    msg = await client.ask(message.chat.id, "**Nᴏᴡ Sᴇɴᴅ Mᴇ Yᴏᴜʀ Fɪʟᴇ/Vɪᴅᴇᴏ Tᴏ Gᴇᴛ Sᴛʀᴇᴀᴍ Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ**")
    if not msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        return await message.reply("**Please send me supported media.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        file_name = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        caption = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {caption}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("🚀 Fᴀsᴛ Dᴏᴡɴʟᴏᴀᴅ 🚀", url=download),  # web download Link
                    InlineKeyboardButton('🖥️ Wᴀᴛᴄʜ Oɴʟɪɴᴇ 🖥️', url=stream)   # web stream Link
                ]]
            )
        )
        rm=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Sᴛʀᴇᴀᴍ 🖥", url=stream),
                InlineKeyboardButton('Dᴏᴡɴʟᴏᴀᴅ 📥', url=download)
            ]] 
        )
        msg_text = """<i><u>✅ 𝗟𝗶𝗻𝗸𝘀 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 !</u></i>\n\n<b>📂 Fɪʟᴇ Nᴀᴍᴇ : <i>{}</i></b>\n\n<b>📦 Fɪʟᴇ Sɪᴢᴇ : <i>{}</i></b>\n\n<b>📥 Fᴀsᴛ Dᴏᴡɴʟᴏᴀᴅ : <i>{}</i></b>\n\n<b> 🖥 Wᴀᴛᴄʜ Oɴʟɪɴᴇ  : <i>{}</i></b>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
