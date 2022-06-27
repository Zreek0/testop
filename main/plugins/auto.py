import os, shutil, logging, time

from ..fast_telethon import download_file, upload_file, uploader
from .pyexec import bash
from telethon.sync import events
from . import *

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

@bot.on(events.NewMessage(from_users=5038395271))
async def nyaa(event):
	timer = Timer()
	msg = await bot.get_messages(event.chat_id, ids=1348)
	async def progress_bar(current, total):
		timer = Timer()
		if timer.can_send():
			await msg.edit("{} {}%".format(type_of, current * 100 / total))
	if event.media and event.message.text.startswith("[SubsPlease]"):
		d = await download_file(event.client, event.document, open(event.file.name, "wb"), progress_callback=progress_bar)
		os.rename(event.file.name, f"{event.id}.mkv")
		ename = event.file.name.replace("[SubsPlease]", "[@Auto_Anime]")
		ename = ename.split(" [")[0] + ".mkv"
		cmd = f"""ffmpeg -i "{event.id}.mkv" -vf subtitles={event.id}.mkv -map 0 -c:v libx265 -crf 28 "{ename}" && echo Done"""
		thumb = await event.message.download_media(thumb=-1)
		ok, err = await bash(cmd)
		if ok:
			u = await upload_file(event.client, open(ename, "rb"), progress_callback=progress_bar)
			pname = ename.replace(" [@Auto_Anime]", "").replace(" (720p).mkv", "")
			await bot.send_file(-1001448819386, u, thumb=thumb, caption=f"**✦ Name:** `{pname}`\n**✦ Quality :** `720p`")
		else:
			logging.getLogger(__name__).info(err)
		os.remove(f"{event.id}.mkv")
		os.remove(ename)
		os.remove(thumb)
