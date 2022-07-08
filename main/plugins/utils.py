import os, io, glob

from telethon.sync import events
from telethon.errors.rpcerrorlist import MessageTooLongError
from pyrogram import filters
from pyrogram import errors
from . import *

def hb(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size

@app.on_message(filters.user(list(SUDOS)) & filters.regex("^/ls ?(.*)"))
async def listdirectory(bot, event):
    files = event.matches[0].group(1)
    if not files:
        files = "*"
    elif files.endswith("/"):
        files += "*"
    elif "*" not in files:
        files += "/*"
    files = glob.glob(files)
    if not files:
        return await event.reply_text("`Directory Empty or Incorrect.`")
    pyfiles = []
    jsons = []
    vdos = []
    audios = []
    pics = []
    others = []
    otherfiles = []
    folders = []
    text = []
    apk = []
    exe = []
    zip_ = []
    book = []
    for file in sorted(files):
        if os.path.isdir(file):
            folders.append("ðŸ“‚ " + str(file))
        elif str(file).endswith(".py"):
            pyfiles.append("ðŸ " + str(file))
        elif str(file).endswith(".json"):
            jsons.append("ðŸ”® " + str(file))
        elif str(file).endswith((".mkv", ".mp4", ".avi", ".gif", "webm")):
            vdos.append("ðŸŽ¥ " + str(file))
        elif str(file).endswith((".mp3", ".ogg", ".m4a", ".opus")):
            audios.append("ðŸ”Š " + str(file))
        elif str(file).endswith((".jpg", ".jpeg", ".png", ".webp", ".ico")):
            pics.append("ðŸ–¼ " + str(file))
        elif str(file).endswith((".txt", ".text", ".log")):
            text.append("ðŸ“„ " + str(file))
        elif str(file).endswith((".apk", ".xapk")):
            apk.append("ðŸ“² " + str(file))
        elif str(file).endswith((".exe", ".iso")):
            exe.append("âš™ " + str(file))
        elif str(file).endswith((".zip", ".rar")):
            zip_.append("ðŸ—œ " + str(file))
        elif str(file).endswith((".pdf", ".epub")):
            book.append("ðŸ“— " + str(file))
        elif "." in str(file)[1:]:
            others.append("ðŸ· " + str(file))
        else:
            otherfiles.append("ðŸ“’ " + str(file))
    omk = [
        *sorted(folders),
        *sorted(pyfiles),
        *sorted(jsons),
        *sorted(zip_),
        *sorted(vdos),
        *sorted(pics),
        *sorted(audios),
        *sorted(apk),
        *sorted(exe),
        *sorted(book),
        *sorted(text),
        *sorted(others),
        *sorted(otherfiles),
    ]
    text = ""
    fls, fos = 0, 0
    flc, foc = 0, 0
    for i in omk:
        try:
            emoji = i.split()[0]
            name = i.split(maxsplit=1)[1]
            nam = name.split("/")[-1]
            if os.path.isdir(name):
                size = 0
                for path, dirs, files in os.walk(name):
                    for f in files:
                        fp = os.path.join(path, f)
                        size += os.path.getsize(fp)
                if hb(size):
                    text += emoji + f" `{nam}`" + "  `" + hb(size) + "`\n"
                    fos += size
                else:
                    text += emoji + f" `{nam}`" + "\n"
                foc += 1
            else:
                if hb(int(os.path.getsize(name))):
                    text += (
                        emoji
                        + f" `{nam}`"
                        + "  `"
                        + hb(int(os.path.getsize(name)))
                        + "`\n"
                    )
                    fls += int(os.path.getsize(name))
                else:
                    text += emoji + f" `{nam}`" + "\n"
                flc += 1
        except BaseException:
            pass
    tfos, tfls, ttol = hb(fos), hb(fls), hb(fos + fls)
    if not hb(fos):
        tfos = "0 B"
    if not hb(fls):
        tfls = "0 B"
    if not hb(fos + fls):
        ttol = "0 B"
    text += f"\n\n`Folders` :  `{foc}` :   `{tfos}`\n`Files` :       `{flc}` :   `{tfls}`\n`Total` :       `{flc+foc}` :   `{ttol}`"
    try:
        await app.send_message(event.chat.id, text, reply_to_message_id=event.id)
    except errors.BadRequest:
        with io.BytesIO(str.encode(text)) as out_file:
            out_file.name = "output.txt"
            await app.send_document(event.chat.id, out_file, reply_to_message_id=event.id)
        await event.delete()
