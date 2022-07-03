import os
import time
import requests
from .uws import *
from telethon.sync import events
from . import *
import cloudscraper
import asyncio

def get_link(link, cloud=None):
	if cloud:
		scraper = cloudscraper.create_scraper()
		r = scraper.get(link)
		r.raise_for_status()
	else:
		r = requests.Session().get(link)
		r.raise_for_status()
	return r.url

@bot.on(events.NewMessage(pattern="/read (-h|-mc|-mh|-ws|-m|-18|-t|-20) ?(.*)", from_users=SUDOS))
async def readpornhwa(event):
	site = event.pattern_match.group(1).strip()
	input_str = event.pattern_match.group(2)
	splited = input_str.split(" | ")
	mess = await eor(event, "`Processing...`")
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
		try:
			pdfname = await post_ws(link, name.title(), ch, class_=class_, src=src)
			xx = await uploader(pdfname, pdfname, time.time(), mess, "")
			await event.client.send_file(event.chat_id, xx)
			os.remove(pdfname)
			await eod(mess, f"Sucessfully uploaded `{name.title()} - Chapter {ch}` from [here]({link})")
		except Exception as e:
			await eod(mess, f"**Error :** `{e}`")
			pass
	elif not input_str or len(splited) < 2:
		await eod(mess, "`Sorry, invalid syntax.`")
		
		
			
			
			
