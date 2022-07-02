from ..sql.globals import gvarstatus, addgvar, delgvar
from . import *
from telethon import events

@bot.on(events.NewMessage(chats=-1001606385356))
async def _(event):
	id = gvarstatus("MID")
	if event.text and "releasing" in event.text.lower() and str(event.id) != str(id):
		addgvar("MID", event.id)
