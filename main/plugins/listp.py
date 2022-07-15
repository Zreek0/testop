import re
from . import *
from telethon import events
from ..sql.globals import gvarstatus

@bot.on(events.NewMessage(pattern="/listp ?(.*)", from_users=SUDOS))
async def getplist(event):
	e = await eor(event, "`Processing...`")
	input_str = event.pattern_match.group(1)
	post = str()
	n = 0
	ids1 = list(range(2, 201))
	ids2 = list(range(2, int(gvarstatus("MID"))))
	mess1 = await app.get_messages("adult_mangas", message_ids=ids1)
	mess2 = await app.get_messages("adult_mangas", message_ids=ids2)
	mess = mess1 + mess2
	for m in mess:
		if m.caption and m.caption_entities and "releasing" in m.caption.lower():
			name = m.caption.split("\n")[0].split(" | ")[0]
			url = m.caption_entities[-1].url
			if input_str.strip() in ["-c", "--channel"]:
				post += f"➤ [{name}]({url})\n"
			else:
				n += 1
				post+= f"{n-1}.] [{name}]({url})\n"
	await eor(e, post)
