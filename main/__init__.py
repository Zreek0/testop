from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events
from config import Config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
bot = TelegramClient("AutoAnime", Config.get("API_ID"), Config.get("API_HASH")).start(bot_token=Config.get("BOT_TOKEN"))
SUDOS = 5038395271, 5370531116, 5074055497
