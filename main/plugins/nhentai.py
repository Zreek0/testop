import re
import os
import random
import requests
import time

from html_telegraph_poster import TelegraphPoster
from asyncio import sleep
from hentai import Hentai, Utils
from natsort import natsorted
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

@bot.on(admin_cmd(pattern="nhentai(?: |$)(.*)", allow_sudo=True))
async def nhentai_(event):
    if event.fwd_from:
        return
    await eor(event, "`Searching for doujin...`")
    input_str = event.pattern_match.group(1)
    code = input_str
    if "nhentai" in input_str:
        link_regex = r"(?:https?://)?(?:www\.)?nhentai\.net/g/(\d+)"
        match = re.match(link_regex, input_str)
        code = match.group(1)
    if input_str == "random":
        code = Utils.get_random_id()
    try:
        doujin = Hentai(code)
    except BaseException as n_e:
        if "404" in str(n_e):
            return await eod(
                event, f"No doujin found for `{code}`. You shouldn't use nhentai :-("
            )
        return await eod(event, f"**ERROR :** `{n_e}`")
    msg = ""
    imgs = "".join(f"<img src='{url}'/>" for url in doujin.image_urls)
    imgs = f"&#8205; {imgs}"
    title = doujin.title()
    graph_link = await post_to_telegraph(title, imgs)
    msg += f"[{title}]({graph_link})\n"
    msg += f"\n**Source :**\n[{code}]({doujin.url})"
    if doujin.parody:
        msg += "\n**Parodies :**"
        parodies = [
            "#" + parody.name.replace(" ", "_").replace("-", "_")
            for parody in doujin.parody
        ]

        msg += "\n" + " ".join(natsorted(parodies))
    if doujin.character:
        msg += "\n**Characters :**"
        charas = [
            "#" + chara.name.replace(" ", "_").replace("-", "_")
            for chara in doujin.character
        ]

        msg += "\n" + " ".join(natsorted(charas))
    if doujin.tag:
        msg += "\n**Tags :**"
        tags = [
            "#" + tag.name.replace(" ", "_").replace("-", "_") for tag in doujin.tag
        ]

        msg += "\n" + " ".join(natsorted(tags))
    if doujin.artist:
        msg += "\n**Artists :**"
        artists = [
            "#" + artist.name.replace(" ", "_").replace("-", "_")
            for artist in doujin.artist
        ]

        msg += "\n" + " ".join(natsorted(artists))
    if doujin.language:
        msg += "\n**Languages :**"
        languages = [
            "#" + language.name.replace(" ", "_").replace("-", "_")
            for language in doujin.language
        ]

        msg += "\n" + " ".join(natsorted(languages))
    if doujin.category:
        msg += "\n**Categories :**"
        categories = [
            "#" + category.name.replace(" ", "_").replace("-", "_")
            for category in doujin.category
        ]

        msg += "\n" + " ".join(natsorted(categories))
    msg += f"\n**Pages :**\n{doujin.num_pages}"
    await eor(event, msg, link_preview=True)

@bot.on(admin_cmd(pattern="nh(?: |$)(.*)", allow_sudo=True))
async def cult(event):
    if event.fwd_from:
        return
    chat = -1001519487732
    e = await eor(event, "`Searching for doujin...`")
    input_str = event.pattern_match.group(1)
    code = input_str
    if "nhentai" in input_str:
        link_regex = r"(?:https?://)?(?:www\.)?nhentai\.net/g/(\d+)"
        match = re.match(link_regex, input_str)
        code = match.group(1)
    if input_str == "random":
        code = Utils.get_random_id()
    try:
        doujin = Hentai(code)
    except BaseException as n_e:
        if "404" in str(n_e):
            return await eod(
                e, f"No doujin found for `{code}`. You shouldn't use nhentai :-("
            )
        return await eod(e, f"**ERROR :** `{n_e}`")
    msg = ""
    imgs = "".join(f"<img src='{url}'/>" for url in doujin.image_urls)
    imgs = f"&#8205; {imgs}"
    title = doujin.title()
    nn = title.split("|")
    pdfname = nn[0] + "@Adult_Mangas.pdf" if len(nn) > 1 else nn[0] + ".pdf"
    graph_link = await post_to_telegraph(title, imgs)
    msg += f"[{title}]({graph_link})\n"
    msg += f"\n➤ **Code :** {code}"
    if doujin.category:
        msg += "\n➤ **Type : **"
        categories = [
            "#" + category.name.replace(" ", "_").replace("-", "_")
            for category in doujin.category
        ]

        msg += " ".join(natsorted(categories))
    if doujin.parody:
        msg += "\n➤ **Parodies : **"
        parodies = [
            "" + parody.name.replace(" ", "_").replace("-", "_")
            for parody in doujin.parody
        ]

        msg += " ".join(natsorted(parodies))
    if doujin.artist:
        msg += "\n➤ **Artists : **"
        artists = [
            "" + artist.name.replace(" ", "_").replace("-", "_")
            for artist in doujin.artist
        ]

        msg += " ".join(natsorted(artists))
    if doujin.language:
        msg += "\n➤ **Languages : **"
        languages = [
            "" + language.name.replace(" ", "_").replace("-", "_")
            for language in doujin.language
        ]

        msg += " ".join(natsorted(languages))
    
    msg += f"\n➤ **Pages : **{doujin.num_pages}"
    if doujin.tag:
        msg += "\n➤ **Tags : **"
        tags = [
            "#" + tag.name.replace(" ", "_").replace("-", "_") for tag in doujin.tag
        ]

        msg += " ".join(natsorted(tags))
    await bash(f"nhentai --id={code} --format={code} -P --rm-origin-dir")
    os.rename(f"{code}.pdf", pdfname)
    pdffile = await uploader(pdfname, pdfname, time.time(), e, "Uploading... " + pdfname)
    mess = await bot.send_message(chat, msg, link_preview=True)
    await bot.send_file(chat, pdffile, caption="**PDF VIEW**", thumb=False)
    smess = await bot.send_file(chat, "CAADAQADRwIAArtf8EeIGkF9Fv05gQI")
    os.remove(pdfname)
    here = f"[{mess.chat.title}](https://t.me/c/{mess.chat.id}/{mess.id})"
    await eor(e, f"**Done Successfully** Sent post in " + here)
