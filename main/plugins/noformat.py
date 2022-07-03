from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate
from . import *

def parse_pre(text):
    text = text.strip()
    return (
        text,
        [MessageEntityPre(offset=0, length=len(add_surrogate(text)), language="")],
    )

@bot.on(admin_cmd("noformat ?(.*)", allow_sudo=True))
async def mono_format(event):
 reply = await event.get_reply_message()
 if not reply:
  await eor(event, "`Reply to a Message...`")
 else:
  await eor(event, reply.text, parse_mode=parse_pre)
