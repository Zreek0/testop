import re
import os
import time
from . import *
from .pyexec import bash
from bs4 import BeautifulSoup
import shutil
import requests
import cloudscraper
import img2pdf
request = requests.Session()

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
		except Exception:
			os.remove(pdfname)
			cmd = await bash(f"convert `ls -tr {upr}/*` mydoc.pdf")
			os.rename("mydoc.pdf", pdfname)
		except:
			raise 
	shutil.rmtree(upr)
	return pdfname
