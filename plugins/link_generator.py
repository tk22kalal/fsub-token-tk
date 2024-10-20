import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot  # Your bot instance
from config import ADMINS, CUSTOM_CAPTION, CHANNEL_ID, CD_CHANNEL
from helper_func import encode, get_message_id
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

# Function to clean captions
def clean_caption(caption):
    caption = re.sub(r'\s?[@#]\S+', '', caption)  # Remove # and @ tags
    caption = re.sub(r'http\S+', '', caption)  # Remove URLs
    return caption

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    # ===== Phase 1: Create Batch Links for Videos =====
    while True:
        try:
            first_message = await client.ask(
                chat_id=message.from_user.id,
                text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link",
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except Exception:
            return  # Timeout or other exception

        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(
                "❌ Error\n\nThis Forwarded Post is not from my DB Channel or the Link is incorrect.", 
                quote=True
            )

    while True:
        try:
            second_message = await client.ask(
                chat_id=message.from_user.id,
                text="Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post Link",
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except Exception:
            return  # Timeout or other exception

        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(
                "❌ Error\n\nThis Forwarded Post is not from my DB Channel or the Link is incorrect.", 
                quote=True
            )

    # Create batch links for videos (Phase 1)
    batch_links = []
    for msg_id in range(min(f_msg_id, s_msg_id), max(f_msg_id, s_msg_id) + 1):
        try:
            string = f"get-{msg_id * abs(client.db_channel.id)}"
            base64_string = await encode(string)
            link = f"https://t.me/{client.username}?start={base64_string}"
            batch_links.append((link, msg_id))
        except Exception as e:
            await message.reply(f"Error generating link for message {msg_id}: {e}")

    # Send batch links to the DB channel and collect message links (Phase 1)
    sent_links = []
    for link, msg_id in batch_links:
        try:
            current_message = await client.get_messages(client.db_channel.id, msg_id)

            # Generate caption
            if bool(CUSTOM_CAPTION) and current_message.document:
                caption = CUSTOM_CAPTION.format(
                    previouscaption=clean_caption(current_message.caption or ""),
                    filename=current_message.document.file_name
                )
            else:
                caption = clean_caption(current_message.caption or "")

            # Send to DB channel and store the message link
            sent_message = await client.send_message(
                chat_id=CHANNEL_ID, 
                text=f"{caption}\n{link}"
            )
            sent_links.append(sent_message.link)  # Store the message link
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(
                chat_id=CHANNEL_ID, 
                text=f"{caption}\n{link}"
            )
        except Exception as e:
            await message.reply(f"Error processing message {msg_id}: {e}")

    await message.reply("✅ Batch processing of videos completed.")

    # ===== Phase 2: Create Batch Link for Sent Batch Links =====
    while True:
        try:
            # Ask the admin for the first and last message link in DB channel (Phase 2)
            first_batch_link_message = await client.ask(
                chat_id=message.from_user.id,
                text="Send the First Message Link from the DB Channel (Batch 1)...",
                timeout=60
            )
            first_batch_msg_id = await get_message_id(client, first_batch_link_message)

            last_batch_link_message = await client.ask(
                chat_id=message.from_user.id,
                text="Send the Last Message Link from the DB Channel (Batch 1)...",
                timeout=60
            )
            last_batch_msg_id = await get_message_id(client, last_batch_link_message)

            break  # Exit the loop if both IDs are valid
        except Exception as e:
            await message.reply(f"Error: {e}. Please try again.")

    # Generate final batch links (Phase 2)
    final_links = []
    for msg_id in range(min(first_batch_msg_id, last_batch_msg_id), max(first_batch_msg_id, last_batch_msg_id) + 1):
        try:
            string = f"get-{msg_id * abs(client.db_channel.id)}"
            base64_string = await encode(string)
            final_link = f"https://t.me/{client.username}?start={base64_string}"
            final_links.append(final_link)
        except Exception as e:
            await message.reply(f"Error generating batch link: {e}")

    # Send the final batch links to the admin
    for final_link in final_links:
        try:
            await client.send_message(
                chat_id=message.from_user.id, 
                text=f"Batch Link: {final_link}"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(
                chat_id=message.from_user.id, 
                text=f"Batch Link: {final_link}"
            )
        except Exception as e:
            await message.reply(f"Error sending final batch link: {e}")

    await message.reply("✅ Batch processing of batch links completed.")
