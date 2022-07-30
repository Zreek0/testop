import re
from . import *
from telethon import events
from .ongoing import pnames
from ..sql.globals import gvarstatus

def get_plist():
	data = dict()
	ids1 = list(range(2, 201))
	ids2 = list(range(201, int(gvarstatus("MID"))))
	mess1 = app.get_messages("adult_mangas", message_ids=ids1)
	mess2 = app.get_messages("adult_mangas", message_ids=ids2)
	mess = mess1 + mess2
	for m in mess:
		if m.caption and m.caption_entities and "releasing" in m.caption.lower():
			name = m.caption.split("\n")[0].split(" | ")[0].strip()
			link = m.caption_entities[-1].url
			data[name] = link
	return data

plist = get_plist()
@bot.on(events.NewMessage(pattern="/listp ?(.*)", from_users=SUDOS))
async def getplist(event):
	e = await eor(event, "`Processing...`")
	input_str = event.pattern_match.group(1)
	post = ""
	n = 0
	for i in pnames:
		if input_str in ["-c", "--channel", "-p", "--post"]:
			post += f"➤ [{i}]({plist[i]})\n"
		else:
			n += 1
			post += f"{n-1}.] [{i}]({plist[i]})\n"
	await eor(e, post)
	
