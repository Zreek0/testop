import asyncio
import io
import os
import sys
import traceback
from telethon.sync import events

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

@bot.on(events.NewMessage(pattern="/exec ?(.*)", from_users=SUDOS))
async def exec_(event):
	e = await event.reply("`Processing...`")
	cmd = "".join(event.message.message.split(maxsplit=1)[1:])
	stdout, stderr = await bash(cmd)
	OUT = f"**✦ Stdin :**\n`{cmd}` \n\n"
	if stderr:
		err = f"**✦ Stderr :**\n `{stderr}` \n\n"
	if stdout:
		out = f"**✦ Stdout :**\n `{stdout}` \n\n"
	if not stdout and not stderr:
		out = f"**✦ Stdout :**\n `Success` \n\n"
	OUT += err + out
	if len(OUT) > 4096:
		td = err + out
		with io.BytesIO(str.encode(td)) as f:
			f.name = "exec.txt"
			await event.client.send_file(event.chat_id, f, allow_cache=False, caption=f"`{cmd}`" if len(cmd) < 998 else None)
			await e.delete()
	else:
		await e.edit(OUT, link_preview=True)
		
		

@bot.on(events.NewMessage(pattern="/eval ?(.*)", from_users=SUDOS))
async def _(event):
    e = await event.reply("`Processing...`")
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await event.reply("`What should i run ?..`")
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
    await event.reply(final_output)
    
async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(_format.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        (
            "async def __aexec(message, event , reply, client, p, chat): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )
    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
    
