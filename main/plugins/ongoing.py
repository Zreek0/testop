import time
import requests
import cloudscraper

from .auws import *
from . import *

pnames = get_names()

def get_link(link, cloud=None):
	if cloud:
		try:
			scraper = cloudscraper.create_scraper()
			r = scraper.get(link)
			r.raise_for_status()
		except:
			raise
	else:
		r = requests.Session().get(link)
		r.raise_for_status()
	return r.url

@bot.on(admin_cmd("uws ?(.*)", allow_sudo=True))
async def _uws(event):
	input_str = event.pattern_match.group(1)
	splited = str(input_str).split(" ")
	mess = await eor(event, "`Processing...`")
	if not input_str or not len(splited) >=2:
		return await eod(mess, "`Sorry, invalid syntax`")
	if input_str.strip().startswith("-"):
		name = pnames[int(splited[1])]
		wname = name.lower().replace(" ", "-").replace("'", "").replace(",", "").replace("’", "").replace("?", "").replace("!", "")
		class_ = "wp-manga-chapter-img"
		src = "src"
		site = splited[0]
		ch = splited[2]
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
			xx = await uploader(pdfname, pdfname, time.time(), event, "")
			await event.client.send_file(-1001783376856, xx)
			os.remove(pdfname)
			await eod(mess, f"**Successfully uploaded** [{name.title()} - Chapter {ch}]({link})")
		except Exception as e:
			await eod(mess, f"**Error :** {str(e)}")
	else:
		name = pnames[int(splited[0])]
		wname = name.lower().replace(" ", "-").replace("'", "").replace(",", "").replace("’", "").replace("?", "").replace("!", "")
		class_ = re.compile("p*")
		src = "src"
		ch = splited[1]
		link = "https://manhwa18.cc/webtoon/" + wname + "/chapter-" + ch
		try:
			pdfname = await post_ws(link, name.title(), ch, class_=class_, src=src)
			await app.send_document(-1001783376856, pdfname)
			os.remove(pdfname)
			await eod(mess, f"**Successfully uploaded** [{name.title()} - Chapter {ch}]({link})")
		except Exception as e:
			await eod(mess, f"**Error :** {str(e)}")
			
			
		
