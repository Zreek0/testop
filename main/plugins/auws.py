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
import glob
import logging
request = requests.Session()
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from reportlab.pdfgen import canvas
from PIL import Image

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

def create_pdf(path, images: list):
	pdf = canvas.Canvas(path)

	for image in images:

		# noinspection PyBroadException
		try:
			with Image.open(image) as img:
				w, h = img.size

		except BaseException:
			continue

		pdf.setPageSize((w, h))  # Set the page dimensions to the image dimensions

		pdf.drawImage(image, x=0, y=0)  # Insert the image onto the current page

		pdf.showPage()  # Create a new page ready for the next image

	pdf.save()

async def post_ws(link, name, chapter, class_="wp-manga-chapter-img", src="src"):
	chno = str(chapter)
	chno = chno.replace("-", ".")
	pdfname = f"./Chapter {chno} {name}" + " @Adult_Mangas.pdf"
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
		download(i, file.name, dict(Referer=link))
		images.append(file.name)
	with open(pdfname, "wb") as f:
		try:
			f.write(img2pdf.convert(images))
		except Exception as err:
			cmd = os.system(f"convert `ls -tr ./{upr}/*` mydoc.pdf")
			os.rename("mydoc.pdf", pdfname)
			logging.info(err)
		except:
			raise 
	shutil.rmtree(upr)
	return pdfname
