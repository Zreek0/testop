import re
import os
import time
from . import *
from .mid import gvarstatus
from bs4 import BeautifulSoup
import shutil
import requests
import threading
import cloudscraper
import img2pdf
import logging
request = requests.Session()
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions



logger = logging.getLogger(__name__)
def get_ids():
	ids = list()
	for i in range(2, int(gvarstatus("MID"))):
		ids.append(i)
	return ids
def get_names_1():
	ids = list()
	for i in range(2, 201):
		ids.append(i)
	mess = app.get_messages("adult_mangas", message_ids=ids)
	names = list()
	for m in mess:
		if m.caption and "releasing" in m.caption.lower():
			names.append(m.caption.split("\n")[0].split("|")[0].strip())
	return names
def get_names_2():
	ids = list()
	for i in range(205, int(gvarstatus("MID"))):
		ids.append(i)
	mess = app.get_messages("adult_mangas", message_ids=ids)
	names = list()
	for m in mess:
		if m.caption and "releasing" in m.caption.lower():
			names.append(m.caption.split("\n")[0].split("|")[0].strip())
	return names

def get_names():
	x = get_names_1()
	x1 = get_names_2()
	names = x + x1
	return names

async def post_ws(link, name, chapter, class_="wp-manga-chapter-img", src="src"):
	chno = str(chapter)
	chno = chno.replace("-", ".")
	pdfname = f"Chapter {chno} {name}" + " @Adult_Mangas.pdf"
	upr = f"manga_{chapter}"
	if not os.path.exists(upr):
		os.mkdir(upr)
	scraper = cloudscraper.create_scraper()
	r = requests.get(link)
	if "hentaidexy" in link or "manhwahub" in link:
		r = scraper.get(link)
		r.raise_for_status()
		content = r.content
	elif "toonily" in link:
		content = scraper.get(link).content
	else:
		r = requests.get(link)
		r.raise_for_status()
		content = r.content
	soup = BeautifulSoup(content, "html.parser")
	image_links = soup.find_all("img", class_)
	n = 0
	images = []
	for i in image_links:
		i = i[src].split("\t")[-1]
		n += 1
		file = open(f"./{upr}/{n}.jpg", "wb")
		threading.Thread(target=download, args=[i, file.name, dict(Referer=link)]).start()
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
