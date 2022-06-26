from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql.globals import *
from . import *

def get_schedule():
	p = "📅 **Today's Anime Schedule**\n\n"
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.add_argument("--no-sandbox")
	browser = webdriver.Chrome(options=options)
	browser.get("https://subsplease.org/schedule")
	try:
		timeout_in_seconds = 10
		WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'schedule-widget-item')))
		timings = browser.find_elements(By.CLASS_NAME, "schedule-widget-time")
		soup = BeautifulSoup(browser.page_source, "html.parser")
		shows = soup.find_all(class_="schedule-widget-show")
	except TimeoutException:
		raise
	
	for (show, atime) in zip(shows, timings):
		p += f'✦ [{show.a.string}](https://SubsPlease.org{show.a["href"]}) - `{atime.text}`\n'
	return p

async def update_schedule():
	post = get_schedule()
	var = gvarstatus("SCHEDULE_POST")
	pin_msg = gvarstatus("PINNED_POST")
	if post != var:
		addgvar("SCHEDULE_POST", post)
		msg = await bot.send_message(-1001448819386, post, link_preview=False)
		if pin_msg:
			pin_msg = int(pin_msg)
			addgvar("PINNED_POST", msg.id)
			pmsg = await bot.get_messages(msg.chat_id, ids=pin_msg)
			await pmsg.unpin()
			await msg.pin()
		await msg.pin()
		
scheduler = AsyncIOScheduler()
scheduler.add_job(update_schedule, "interval", minutes=60)
scheduler.start()
