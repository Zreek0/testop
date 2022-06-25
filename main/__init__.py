from telethon import TelegramClient
from config import Config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = TelegramClient("AutoAnime", Config.get("API_ID"), Config("API_HASH")).start(BOT_TOKEN=Config.get("BOT_TOKEN"))
