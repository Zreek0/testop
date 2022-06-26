import os, shutil, logging

from ..fast_telethon import downloader, uploader
from .pyexec import bash
from telethon.sync import events
from . import *

logs = logging.getLogger(__name__)
@bot.on(events.NewMessage(from_users=5038395271))
async def nyaa(event):
	if event.media and event.message.text.startswith("[SubsPlease]"):
		d = await downloader(bot, event)
		os.rename(event.file.name, f"{event.id}.mkv")
		ename = event.file.name.replace("[SubsPlease]", "[@Auto_Anime]")
                ename = ename.split(" [")[0] + ".mkv"
		cmd = f"""ffmpeg -i "{event.id}.mkv" -vf subtitles={event.id}.mkv -map 0 -c:v libx265 -crf 28 "{ename}" && echo Done"""
		thumb = await event.download_media(thumb=-1)
		ok, err = await bash(cmd)
		if ok:
			u = await uploader(bot, ename)
			pname = ename.replace("[@Auto_Anime]", "").replace(" (720p).mkv")
			await bot.send_file(-1001448819386, u, thumb=thumb, caption=f"**✦ Name:** `{pname}`\n**✦ Quality :** `720p`")
		else:
			logs.info(err)
		os.remove(f"{event.id}.mkv")
		os.remove(ename)
		os.remove(thumb)
