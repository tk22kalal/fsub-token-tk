from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from config import CHANNEL_ID

class CustomClient(Client):
    def __init__(self, db_channel, *args, **kwargs):
        self.db_channel = db_channel
        super().__init__(*args, **kwargs)
