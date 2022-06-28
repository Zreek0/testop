import os, shutil, logging, time

from ..fast_telethon import download_file, upload_file, uploader
from .pyexec import bash
from telethon.sync import events
import logging
from . import *
from ..sql.globals import gvarstatus, addgvar
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon.tl import types

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)


class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

async def handle_subsplease(event):
	timer = Timer()
	msg = await bot.get_messages(event.chat_id, ids=1348)
	async def progress_bar(current, total):
		timer = Timer()
		if timer.can_send():
			await msg.edit("{} {}%".format(type_of, current * 100 / total))
	if event.file and event.text.startswith("[SubsPlease]"):
		d = await download_file(bot, event.document, open(event.file.name, "wb"), progress_callback=progress_bar)
		os.rename(event.file.name, f"{event.id}.mkv")
		ename = event.file.name.replace("[SubsPlease]", "[@Ongoing_Seasonal_Anime]")
		ename = ename.split(" [")[0] + ".mp4"
		cmd = f"""ffmpeg -i "{event.id}.mkv" -vf subtitles={event.id}.mkv -map 0:v -map 0:a -c:v libx264 -map 0:s -c:s mov_text -crf 28 "{ename}" && echo Done"""
		thumb = await event.message.download_media(thumb=-1)
		ok, err = await bash(cmd)
		if ok:
			u = await upload_file(event.client, open(ename, "rb"), progress_callback=progress_bar)
			pname = ename.replace("[@Ongoing_Seasonal_Anime] ", "").replace(" (720p).mp4", "")
			await bot.send_file(-1001448819386, u, thumb=thumb, caption=f"**{pname}**\n\n**✦ Audio :** `Japanese`\n**✦ Subtitles :** `English`\n**✦ Quality :** `720p`", supports_streaming=True)
		else:
			logging.getLogger(__name__).info(err)
		os.remove(f"{event.id}.mkv")
		os.remove(ename)
		os.remove(thumb)

async def auto_anime():
	post = gvarstatus("ANIME_POST")
	m = await zreek.get_messages(-1001718753693, filter=types.InputMessagesFilterDocument, limit=1)
	m = m[0]
	if m.text and m.text.startswith("[SubsPlease]") and m.text != post:
		addgvar("ANIME_POST", m.text)
		await m.forward_to(m.chat_id)
		await handle_subsplease(m)


scheduler = AsyncIOScheduler()
scheduler.add_job(auto_anime, "interval", minutes=1)
scheduler.start()
