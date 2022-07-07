from ..sql.globals import gvarstatus, addgvar, delgvar
from . import *
from .uws import get_names
from telethon import events

@bot.on(events.NewMessage(chats="adult_mangas"))
async def _mid(event):
	if event.text and "releasing" in event.message.lower():
		addgvar("MID", event.id)
		names = await get_names()
		addgvar("GET_NAMES", names)
	
