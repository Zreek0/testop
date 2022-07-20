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
from concurrent.futures import ThreadPoolExecutor
from undetected_chromedriver import ChromeOptions
from reportlab.pdfgen import canvas
from PIL import Image

logger = logging.getLogger(__name__)
def get_names():
	names = []
	ids1 = list(range(2, 201))
	ids2 = list(range(201, int(gvarstatus("MID"))))
	mess1 = app.get_messages("adult_mangas", message_ids=ids1)
	mess2 = app.get_messages("adult_mangas", message_ids=ids2)
	mess = mess1 + mess2
	for m in mess:
		if m.photo and m.caption and "releasing" in m.caption.lower():
			names.append(m.caption.split("\n")[0].split(" | ")[0])
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
	upr = f"manga{chapter}"
	if not os.path.exists(upr):
		os.mkdir(upr)
	scraper = cloudscraper.create_scraper()
	r = requests.get(link)
	if "hentaidexy" in link or "manhwahub" in link:
		r = scraper.get(link)
		r.raise_for_status()
	elif "toonily" in link:
		r = scraper.get(link)
	else:
		r = requests.get(link)
		r.raise_for_status()
	soup = BeautifulSoup(r.text, "html.parser")
	image_links = soup.find_all("img", class_)
	n = 0
	images = []
	for i in image_links:
		i = i[src].split("\t")[-1]
		n += 1
		file = open(f"./{upr}/{n}.jpg", "wb")
		await fast_download(i, filename=file.name, headers=dict(Referer=r.url))
		images.append(file.name)
	with open(pdfname, "wb") as f:
		try:
			f.write(img2pdf.convert(images))
		except Exception as err:
			cmd = os.system(f"convert `ls -tr {upr}/` mydoc.pdf")
			os.rename("mydoc.pdf", pdfname)
			logging.info(err)
		except:
			raise 
	shutil.rmtree(upr)
	return pdfname

def h20(): 
 args = dict()
 r = cloudscraper.create_scraper().get("https://Hentai20.com/")
 r.raise_for_status()
 soup = BeautifulSoup(r.text, "html.parser")
 data = soup.find("div", "c-blog-listing c-page__content manga_content").find("a")
 args["title"] = data["title"]
 link = None
 data_link = soup.find_all("a", href=re.compile(data["href"]))
 data_link.remove(data_link[0])
 data_link.remove(data_link[0])
 args["link"] = data_link[0]["href"]
 ch_input = data_link[0].string.strip()
 ch_regex = r"[^.]hapter (\d+)"
 match = re.match(ch_regex, ch_input)
 args["ch"] = match.group(1)
 return args
class nhentai:
	def __init__(self, link):
		if "hentai" in link:
			link = link
			code_regex = r"(?:https?://)?(?:www\.)?nhentai\.to/g/(\d+)"
			self.code = re.match(code_regex, link).group(1)
		else:
			self.code = code = link
			link = f"https://nhentai.to/g/{code}/"
		response = requests.get(link)
		response.raise_for_status()
		soup = BeautifulSoup(response.text, "html.parser")
		self.title = soup.find("div", id="info").find("h1").text
		self.tags = []
		self.artists = []
		self.parodies = []
		self.categories = []
		self.languages = []
		self.images = []
		self.url = response.url
		tdata = soup.find_all("a", "tag")
		for t in tdata:
			if "tag" in t["href"]:
				self.tags.append("#"+t.text.replace(" ", "_").replace("-", "_"))
			elif "artist" in t["href"]:
				self.artists.append(t.text.replace(" ", "_"))
			elif "parody" in t["href"]:
				self.parodies.append(t.text.replace(" ", "_"))
			elif "language" in t["href"]:
				self.languages.append(t.text.replace(" " , "_"))
			elif "category" in t["href"]:
				self.categories.append("#"+t.text.replace(" ", "_"))
		data = soup.find_all("img", "lazyload")
		for i in data:
			i = i["data-src"].split("\t")[-1].replace("t.", ".")
			self.images.append(i)
			pass
		self.pages = len(self.images)
