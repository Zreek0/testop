import re
import os
import random
import requests
import time

from html_telegraph_poster import TelegraphPoster
from asyncio import sleep
from hentai import Hentai, Utils
from natsort import natsorted
from .auws import img2pdf, nhentai

from . import *

def media_type(message):
    if message and message.photo:
        return "Photo"
    if message and message.audio:
        return "Audio"
    if message and message.voice:
        return "Voice"
    if message and message.video_note:
        return "Round Video"
    if message and message.gif:
        return "Gif"
    if message and message.sticker:
        return "Sticker"
    if message and message.video:
        return "Video"
    if message and message.document:
        return "Document"
    return None


async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "@Adult_Mangas"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url="https://t.me/Adult_Mangas",
        text=html_format_content,
    )
    return post_page["url"]

async def images_to_pdf(images: list, pdfname: str, dir="nhentai", headers=None):
	if not os.path.exists(dir):
		os.mkdir(dir)
	image_list = []
	for link in images:
		name = "./" + dir + "/" + link.split("/")[-1]
		await fast_download(link, filename=name, headers=headers)
		image_list.append(name)
	with open(os.getcwd()+"/"+pdfname, "wb") as file:
		file.write(img2pdf.convert(image_list))
		file.close()
	shutil.rmtree(dir)
	return file.name

@bot.on(admin_cmd(pattern="nh(?: |$)(.*)", allow_sudo=True))
async def _(event):
	chat = -1001519487732
	m = await eor(event, "`Processing ...`")
	input_str = event.pattern_match.group(1)
	if not input_str:
		return await eod(m, "`Give any Doujin to upload for...`")
	try:
		doujin = nhentai(input_str)
	except Exception as e:
		await eod(m, f"**Error :** `{e}`")
		return
	msg = ""
	imgs =  "".join(f"<img src='{url}'/>" for url in doujin.images)
	title = doujin.title
	nn = title.split("|")
	pdfname = nn[0].strip() + " @Adult_Mangas.pdf" if len(nn) > 1 else nn[0] + ".pdf"
	graph_link = await post_to_telegraph(title, imgs)
	msg += f"[{title}]({graph_link})\n"
	msg += f"\n➤ **Code :** {doujin.code}"
	if doujin.categories:
		msg += "\n➤ **Type : **"
		msg += " ".join(natsorted(doujin.categories))
	if doujin.parodies:
		msg += "\n➤ **Parodies : **"
		msg += " ".join(natsorted(doujin.parodies))
	if doujin.artists:
		msg += "\n➤ **Artists : **"
		msg += " ".join(natsorted(doujin.artists))
	if doujin.languages:
		msg += "\n➤ **Languages : **"
		msg += " ".join(natsorted(doujin.languages))
	msg += f"\n➤ **Pages : ** {doujin.pages}"
	if doujin.tags:
		msg += "\n➤ **Tags : **"
		msg += " ".join(natsorted(doujin.tags))
	file = await images_to_pdf(doujin.images, pdfname, dir=doujin.code, headers=dict(Referer=doujin.url))
	mess = await bot.send_message(chat, msg, link_preview=True)
	await app.send_document(chat, file, caption="**PDF VIEW**")
	await bot.send_file(chat, "CAADAQADRwIAArtf8EeIGkF9Fv05gQI")
	os.remove(file)
	here = f"[{mess.chat.title}](https://t.me/c/{mess.chat.id}/{mess.id})"
	await eor(m, f"**Done Successfully** Sent post in {here}")
    	
