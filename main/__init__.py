from telethon import TelegramClient
from config import Config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)

bot = TelegramClient("AutoAnime", Config.get("API_ID"), Config.get("API_HASH")).start(bot_token=Config.get("BOT_TOKEN"))
SUDOS = 5038395271, 5370531116
