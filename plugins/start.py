# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de
# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import re
import os
import random
import asyncio
import pymongo
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pymongo import MongoClient
from bot import Bot
from config import DB_URI as MONGO_URL
from config import (
    ADMINS,
    CUSTOM_CAPTION,
    DISABLE_CHANNEL_BUTTON,
    FORCE_MSG,
    PROTECT_CONTENT,
    DB_NAME,
    DB_URI,
    START_MSG,
    API_ID,
    API_HASH,
)
from database.mongo import collection, adds_user, del_user, fulls_userbase, present_user
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, WebAppInfo

from helper_func import decode, get_messages
from helper import b64_to_str, str_to_b64, get_current_time

# MongoDB setup
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]
referral_collection = mongo_db["referrals"]
video_requests = mongo_db["video_requests"]

# Limits and referral settings
MAX_VIDEOS_PER_DAY = 30
TIME_LIMIT = timedelta(hours=24)
REFERRAL_BONUS_THRESHOLD = 5  # Referrals needed to increase video limit

SECONDS = int(os.getenv("SECONDS", "10"))  # Waiting time before delete

async def record_video_request(user_id: int):
    now = datetime.utcnow()
    video_requests.insert_one({"user_id": user_id, "timestamp": now})

def has_exceeded_limit(user_id: int):
    now = datetime.utcnow()
    start_time = now - TIME_LIMIT
    request_count = video_requests.count_documents({
        "user_id": user_id,
        "timestamp": {"$gte": start_time}
    })
    return request_count >= MAX_VIDEOS_PER_DAY

async def generate_referral_code(user_id):
    return f"https://t.me/mynextpulseX_bot?start=ref_{user_id}"

async def get_total_referrals(user_id):
    return referral_collection.count_documents({"referred_by": user_id})

async def increment_max_videos(user_id):
    user_data = referral_collection.find_one({"user_id": user_id})
    if user_data:
        new_limit = min(user_data.get("MAX_VIDEOS_PER_DAY", MAX_VIDEOS_PER_DAY) + 1, 100)
        referral_collection.update_one(
            {"user_id": user_id},
            {"$set": {"MAX_VIDEOS_PER_DAY": new_limit}},
            upsert=True
        )

async def handle_new_referral(referred_by, new_user_id):
    if not await present_user(new_user_id):
        referral_collection.insert_one({"user_id": new_user_id, "referred_by": referred_by})
        await adds_user(new_user_id)
        total_referrals = await get_total_referrals(referred_by)
        if total_referrals % REFERRAL_BONUS_THRESHOLD == 0:
            await increment_max_videos(referred_by)

async def schedule_deletion(msgs, delay):
    await asyncio.sleep(delay)
    for msg in msgs:
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

@Bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Bot, message: Message):
    user_id = message.from_user.id
    referral_code = message.text.split("_")[-1] if "ref_" in message.text else None

    if referral_code and referral_code.isdigit():
        referred_by = int(referral_code)
        if referred_by != user_id:
            await handle_new_referral(referred_by, user_id)

    # Inline button to share referral link
    referral_buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Get Referral Link", callback_data="get_referral_link")]]
    )

    
    if len(message.text) > 7:
        try:
            base64_string = message.text.split(" ", 1)[1]
        except BaseException:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except BaseException:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except BaseException:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception:
            await message.reply_text("Something went wrong..!")
            return
        finally:
            await temp_msg.delete()

        replacement_urls = [
            "https://t.me/testingdoubletera_bot?",
            "https://t.me/Mynextpulsembbs_bot?"
        ]

        snt_msgs = []
        for msg in messages:
            if msg.text and "https://t.me/{\"X\"}?" in msg.text:
                replacement_url = random.choice(replacement_urls)
                msg.text = msg.text.replace("https://t.me/{\"X\"}?", replacement_url)
            if msg.caption and "https://t.me/{\"X\"}?" in msg.caption:
                replacement_url = random.choice(replacement_urls)
                msg.caption = msg.caption.replace("https://t.me/{\"X\"}?", replacement_url)

            caption = (CUSTOM_CAPTION.format(
                previouscaption=msg.caption.html if msg.caption else "",
                filename=msg.document.file_name
            ) if bool(CUSTOM_CAPTION) and bool(msg.document) else
            msg.caption.html if msg.caption else "")

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                snt_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    protect_content=PROTECT_CONTENT,
                    reply_markup=reply_markup,
                )
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
                await record_video_request(user_id)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    protect_content=PROTECT_CONTENT,
                    reply_markup=reply_markup,
                )
                snt_msgs.append(snt_msg)
            except BaseException:
                pass

        asyncio.create_task(schedule_deletion(snt_msgs, SECONDS))
    else:
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}" if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=referral_buttons,
            disable_web_page_preview=True,
            quote=True,
        )

    return
                
@Bot.on_callback_query(filters.regex("get_referral_link"))
async def send_referral_link(client: Bot, callback_query):
    user_id = callback_query.from_user.id
    referral_link = await generate_referral_code(user_id)
    total_referrals = await get_total_referrals(user_id)
    user_data = referral_collection.find_one({"user_id": user_id})
    max_videos = user_data.get("MAX_VIDEOS_PER_DAY", MAX_VIDEOS_PER_DAY) if user_data else MAX_VIDEOS_PER_DAY

    await callback_query.message.reply_text(
        text=(
            f"👤 User ID: **{user_id}**\n"
            f"🔗 Your Referral Link: `{referral_link}`\n"
            f"🌟 Total Referrals: **{total_referrals}**\n"
            f"📹 Daily Video Limit: **{max_videos}**"
        ),
        disable_web_page_preview=True,
        quote=True,
    )

@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Bot, message: Message):
    buttons = fsub_button(client, message)
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else None,
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command(["users", "stats"]) & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(
        chat_id=message.chat.id, text="<code>Processing ...</code>"
    )
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply(
            "<i>Broadcasting Message.. This will Take Some Time</i>"
        )
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(
            "<code>Use this command as a replay to any telegram message with out any spaces.</code>"
        )
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "<b>PONG!!</b>🏓 \n"
        f"<b>• Pinger -</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"<b>• Uptime -</b> <code>{uptime}</code>\n"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 <b>Bot Status:</b>\n"
        f"• <b>Uptime:</b> <code>{uptime}</code>\n"
        f"• <b>Start Time:</b> <code>{START_TIME_ISO}</code>"
    )
