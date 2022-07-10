from ..sql.globals import gvarstatus, addgvar, delgvar
from . import *
from .auws import *
from pyrogram import filters

@app.on_message(filters.chat(-1001606385356) & filters.caption)
async def _mid(client, event):
	if event.caption and "RELEASING" in event.caption:
		addgvar("MID", event.id)
