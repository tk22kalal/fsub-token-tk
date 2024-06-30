# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
import asyncio
import re
import sqlite3
import logging
from tenacity import retry, wait_fixed, stop_after_attempt
from pymongo import MongoClient
from Script import script
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from config import API_ID, API_HASH, ADMINS, DB_NAME
from config import DB_URI as MONGO_URL

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]
mongo_collection = mongo_db[DB_NAME]

buttonz = ReplyKeyboardMarkup(
    [
        ["CLONE"],
    ],
    resize_keyboard=True
)

@Client.on_message(filters.command("clone") & filters.private)
async def clone(client, message):
    await message.reply_text(script.CLONE_TXT)



@Client.on_message((filters.regex(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
async def on_clone(client, message):  
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)
        bots = list(mongo_db.bots.find())
        bot_tokens = None  # Initialize bot_tokens variable

        for bot in bots:
            bot_tokens = bot['token']

        forward_from_id = message.forward_from.id if message.forward_from else None
        if bot_tokens == bot_token and forward_from_id == 93372553:
            await message.reply_text("**©️ ᴛʜɪs ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ʙᴀʙʏ 🐥**")
            return

        if not forward_from_id != 93372553:
            msg = await message.reply_text("**👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️**")
            try:
                ai = Client(
                    f"{bot_token}", API_ID, API_HASH,
                    bot_token=bot_token,
                    plugins={"root": "clone_plugins"},
                )
                
                await ai.start()
                bot = await ai.get_me()
                details = {
                    'bot_id': bot.id,
                    'is_bot': True,
                    'user_id': user_id,
                    'name': bot.first_name,
                    'token': bot_token,
                    'username': bot.username
                }
                mongo_db.bots.insert_one(details)
                await msg.edit_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.</b>")
            except BaseException as e:
                logging.exception("Error while cloning bot.")
                await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @talktomembbs_bot to get assistance.**")
    except Exception as e:
        logging.exception("Error while handling message.")

@Client.on_message(filters.command("deletecloned") & filters.private)
async def delete_cloned_bot(client, message):
    try:
        bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
        bot_token = bot_token[0] if bot_token else None
        bot_id = re.findall(r'\d[0-9]{8,10}', message.text)

        mongo_collection = mongo_db.bots
        
        cloned_bot = mongo_collection.find_one({"token": bot_token})
        if cloned_bot:
            mongo_collection.delete_one({"token": bot_token})
            await message.reply_text("**🤖 ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ʟɪsᴛ ᴀɴᴅ ɪᴛs ᴅᴇᴛᴀɪʟs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ. ☠️**")
        else:
            await message.reply_text("**⚠️ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴘʀᴏᴠɪᴅᴇᴅ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪsᴛ.**")
    except Exception as e:
        logging.exception("Error while deleting cloned bot.")
        await message.reply_text("An error occurred while deleting the cloned bot.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegra
database_lock = asyncio.Lock()

# Use a lock for serializing database access
import logging
from tenacity import retry, wait_fixed, stop_after_attempt
import sqlite3

# Define a logger
logger = logging.getLogger(__name__)

# Retry decorator setup
retry_decorator = retry(stop=stop_after_attempt(5), wait=wait_fixed(2))

@retry_decorator
async def restart_bots():
    logger.info("Restarting all bots........")
    bots = list(mongo_db.bots.find())
    for bot in bots:
        bot_token = bot['token']
        try:
            async with database_lock:
                async with Client(
                    f"{bot_token}", API_ID, API_HASH,
                    bot_token=bot_token,
                    plugins={"root": "clone_plugins"},
                ) as ai:
                    if ai.is_connected:
                        logger.warning(f"Bot with token {bot_token} is already connected.")
                        continue  # Skip to the next bot if already connected

                    await ai.start()
        except sqlite3.OperationalError as e:
            logger.warning(f"SQLite OperationalError encountered: {e}")
            continue  # Skip to the next bot on OperationalError
        except Exception as e:
            # Suppress warnings about already connected bots from being treated as errors
            if "already connected" in str(e):
                logger.warning(f"Bot with token {bot_token} is already connected.")
            else:
                logger.error(f"Error while restarting bot with token {bot_token}: {e}")
            continue  # Skip to the next bot on any other error
