import re
import os
import time
from . import *
from .mid import gvarstatus
from bs4 import BeautifulSoup
import shutil
import requests
import cloudscraper
import img2pdf
import logging
request = requests.Session()

logger = logging.getLogger(__name__)
def get_ids():
	ids = list()
	for i in range(2, int(gvarstatus("MID"))):
		ids.append(i)
	return ids

async def get_names():
	ids = get_ids()
	mess = await bot.get_messages("adult_mangas", ids=ids)
	names = []
	for m in mess:
		if m and m.photo and m.text and "releasing" in m.message.lower():
			name = m.message.split("\n")[0].split(" | ")[0]
			names.append(name)
	return names

async def post_ws(link, name, chapter, class_="wp-manga-chapter-img", src="src"):
	chno = str(chapter)
	chno = chno.replace("-", ".")
	pdfname = f"Chapter {chno} {name}" + " @Adult_Mangas.pdf"
	upr = f"{chapter}"
	if not os.path.exists(upr):
		os.mkdir(upr)
	scraper = cloudscraper.create_scraper()
	r = requests.get(link)
	if "hentaidexy" in link or "manhwahub" in link:
		r = scraper.get(link)
	r.raise_for_status()
	soup = BeautifulSoup(r.content, "html.parser")
	image_links = soup.find_all("img", class_)
	n = 0
	images = []
	for i in image_links:
		i = i[src].split("\t")[-1]
		n += 1
		file = open(f"{upr}/{n}.jpg", "wb")
		file.write(requests.get(i, headers={"Referer": r.url}).content)
		images.append(file.name)
	with open(pdfname, "wb") as f:
		try:
			f.write(img2pdf.convert(images))
		except Exception as err:
			os.remove(pdfname)
                        logger.exception(err)
			cmd = await bash(f"convert `ls -tr {upr}/*` mydoc.pdf")
			os.rename("mydoc.pdf", pdfname)
		except:
			raise 
	shutil.rmtree(upr)
	return pdfname
