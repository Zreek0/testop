import os
import time
import requests
from .auws import *
from telethon.sync import events
from . import *
import cloudscraper
import asyncio
from .ongoing import h20_search

def get_link(link, cloud=None):
	if cloud:
		scraper = cloudscraper.create_scraper()
		r = scraper.get(link)
		r.raise_for_status()
	else:
		r = requests.Session().get(link)
		r.raise_for_status()
	return r.url

@bot.on(admin_cmd(pattern="read (-h|-mc|-mh|-ws|-m|-18|-t|-20) ?(.*)", allow_sudo=True))
async def readpornhwa(event):
	site = event.pattern_match.group(1)
	input_str = event.pattern_match.group(2)
	splited = input_str.split(" | ")
	mess = await eor(event, "`Processing...`")
	if not site:
		return await eod(event, '`Sorry, invalid syntax.`')
	if input_str and len(splited) == 2:
		name = splited[0]
		ch = splited[1]
		wname = name.lower().replace(" ", "-").replace("'", "").replace("’", "").replace("!", "").replace("?", "").replace(",", "")
		class_ = "wp-manga-chapter-img"
		src = "src"
		if site == "-h":
			link = "https://hentaidexy.com/reads/" + wname + "/chapter-" + ch
		elif site == "-mc":
			link = "https://manhwaclub.net/manga/" + wname
			link = get_link(link) + "chapter-" + ch
		elif site == "-mh":
			link = "https://manhwahentai.me/webtoon/" + wname
			link = get_link(link) + "chapter-" + ch
		elif site == "-ws":
			link = "https://webtoonscan.com/manhwa/" + wname + "/" + ch
		elif site == "-m":
			link = "https://manhwahub.net/webtoon/" + wname
			link = get_link(link, cloud=True) + "/chapter-" + ch
			class_ = "chapter-img img-responsive"
		elif site == "-18":
			link = "https://manhwa18.cc/webtoon/" + wname + "/chapter-" + ch
			class_ = re.compile("p*")
		elif site == "-t":
			link = "https://toonily.com/webtoon/" + wname + "/chapter-" + ch
			class_ = "wp-manga-chapter-img img-responsive lazyload effect-fade"
			src = "data-src"
		elif site == "-20":
			try:
				link = h20_search(wname.replace("-", "+"))
				link = link + "chapter-" + ch
			except Exception as e:
				return await eod(mess, f"**Error :** `{e}`")
		try:
			pdfname = await post_ws(link, name.title(), ch, class_=class_, src=src)
			await app.send_document(event.chat_id, pdfname)
			os.remove(pdfname)
			await eod(mess, f"Sucessfully uploaded `{name.title()} - Chapter {ch}` from [here]({link})")
		except Exception as e:
			await eod(mess, f"**Error :** `{e}`")
