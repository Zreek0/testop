import re
from . import *
from telethon import events
from .auws import get_ids

ids = get_ids()
@bot.on(events.NewMessage(pattern="/listp ?(.*)", from_users=SUDOS))
async def getplist(event):
	e = await eor(event, "`Processing...`")
	input_str = event.pattern_match.group(1)
	mess = await app.get_messages("adult_mangas", message_ids=ids)
	post = str()
	n = 0
	for m in mess:
		if m.caption and "releasing" in m.caption.lower():
			name = m.caption.split("\n")[0].split(" | ")[0]
			url = m.caption_entities[-1].url
			if input_str.strip() in ["-c", "--channel"]:
				post += f"➤ [{name}]({url})\n"
			else:
				n += 1
				post += f"{n-1}.] [{name}]({url})"
	await eor(e, post)
	
