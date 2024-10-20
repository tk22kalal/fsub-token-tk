import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot  # Your bot instance
from config import ADMINS, CUSTOM_CAPTION, CHANNEL_ID
from helper_func import encode
from pyrogram.errors import FloodWait

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

        f_msg_id = first_message.forward_from_message_id or int(first_message.text.split("/")[-1])
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Invalid message. Please try again.", quote=True)

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

        s_msg_id = second_message.forward_from_message_id or int(second_message.text.split("/")[-1])
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Invalid message. Please try again.", quote=True)

    # Create batch links for videos (Phase 1)
    batch_links = []
    total_messages = 0  # Track the number of generated messages for Phase 2
    for msg_id in range(min(f_msg_id, s_msg_id), max(f_msg_id, s_msg_id) + 1):
        try:
            string = f"get-{msg_id * abs(client.db_channel.id)}"
            base64_string = await encode(string)
            link = f"https://t.me/{client.username}?start={base64_string}"
            batch_links.append((link, msg_id))

            # Send to the DB channel
            await client.send_message(CHANNEL_ID, text=f"Video Link: {link}")
            total_messages += 1  # Increment the message count
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            await message.reply(f"Error generating link for message {msg_id}: {e}")

    await message.reply("✅ Phase 1 batch processing completed.")

    # ===== Phase 2: Create Batch Links of Batch Links =====
    try:
        # Calculate the first message ID for Phase 2 batch
        first_batch2_msg_id = s_msg_id + 1  # Start right after the last message of Phase 1
        last_batch2_msg_id = s_msg_id + total_messages  # Last message based on total generated in Phase 1

        # Create batch links of batch links (Phase 2)
        final_links = []
        for msg_id in range(first_batch2_msg_id, last_batch2_msg_id + 1):
            try:
                string = f"get-{msg_id * abs(client.db_channel.id)}"
                base64_string = await encode(string)
                final_link = f"https://t.me/{client.username}?start={base64_string}"
                final_links.append(final_link)
            except Exception as e:
                await message.reply(f"Error generating batch link: {e}")

        # Send the final batch links to the admin
        for final_link in final_links:
            await client.send_message(message.from_user.id, text=f"Batch Link: {final_link}")

        await message.reply("✅ Phase 2 batch processing completed.")
    except Exception as e:
        await message.reply(f"Error during Phase 2: {e}")
