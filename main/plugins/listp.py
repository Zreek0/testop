import re
from . import *
from .uws import get_ids

@bot.on(event.NewMessage(pattern="/listp ?(.*)", from_users=SUDOS))
async getplist(event):
	e = await bot.send_message(event.chat_id, "`Processing...`", reply_to=event.id)
	input_str = event.pattern_match.group(1)
	mess = await bot.get_messages(-1001606385356, ids=get_ids())
	post = str()
	n = 0
	for m in mess:
		if m and m.photo and m.text and "releasing" in m.message.lower():
			name = m.message.split("\n")[0].split(" | ")[0]
			links = re.findall("[^.]ttps://t.me/.*", mess.text)[0].replace(")", "")
			link = links.replace(" [New Link]", "")
			if input_str in ["-c", "--channel"]:
				post += f"➤ [{name}]({link})\n"
			else:
				n += 1
				post += f"{n-1}.] [{name}]({link})\n"
	await e.edit(post, link_preview=True)
