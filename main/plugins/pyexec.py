import asyncio
import io
import os
import sys
import traceback
from telethon import events

from config import Config
from . import *

async def bash(cmd, run_code=0):
    """
    run any command in subprocess and get output or error."""
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip() or None
    out = stdout.decode().strip()
    if not run_code and err:
        split = cmd.split()[0]
        if f"{split}: not found" in err:
            return out, f"{split.upper()}_NOT_FOUND"
    return out, err

@bot.on(events.NewMessage(pattern="/eval ?(.*)", from_users=SUDOS))
async def evaluate_(event):
    e = await event.reply("`Processing...`")
    cmd = "".join(event.message.text.split(maxsplit=1)[1:])
    if not cmd:
        return await e.edit("`Give something to excute..`")
    cmd = (
        cmd.replace("send_message", "send_message")
        .replace("send_file", "send_file")
        .replace("edit_message", "edit_message")
    )
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        f"**✦ Eval : **\n```{cmd}``` \n\n**✦  Result : **\n```{evaluation}``` \n"
    )
    if len(final_output) > 4096:
    	with io.BytesIO(str.encode(final_output)) as file:
    		file.name = "eval.txt"
    		await bot.send_file(event.chat_id, file, allow_cache=False)
    		await e.delete()
    else:
    	await e.edit(final_output, link_preview=True)
async def aexec(code, event):
    exec(
        (
            "async def __aexec(e, client): "
            + "\n print = p = _stringify"
            + "\n message = event = e"
            + "\n reply = await event.get_reply_message()"
            + "\n chat = event.chat_id"
        )
        + "".join(f"\n {l}" for l in code.split("\n"))
    )

    return await locals()["__aexec"](event, event.client)
