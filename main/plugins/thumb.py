import os
from . import *
from telethon import events

@bot.on(events.NewMessage("/thumbnail ?(.*)", from_users=SUDOS))
async def _thumb(event):
	r = await event.get_reply_message()
	if r.photo:
		await r.download_media("thumb.jpg")
		await event.reply("`Custom thumbnail set.`")
	elif r.document and r.document.thumbs:
		thumb = await r.download_media(thumb=-1)
		os.rename(thumb, "thumb.jpg")
		await event.reply("`Custom thumbnail set.`")
	else:
		await event.reply("`Reply to Photo or media with thumb...`")
	
