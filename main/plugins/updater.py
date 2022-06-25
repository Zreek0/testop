import os, sys

from .pyexec import bash
from . import *

@bot.on(events.NewMessage("/update$", from_users=SUDOS))
async update_soft(event):
	e = await event.reply("`Fast Soft Updating...`")
	ok, err = await bash("git pull -f && pip install -r requirements.txt")
	os.execl(sys.executable, "python3", "-m", "main")
	if err:
		await e.edit("`Updated repository with some unexpected errors.`")
	else:
		await e.edit("`Sucessfully soft updated plugins and requirements.`")
		
