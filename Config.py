from os import getenv

class Config(object):
	API_ID = getenv("API_ID")
	API_HASH = getenv("API_HASH")
	BOT_TOKEN = getenv("BOT_TOKEN")
	TSESSION = getenv("TSESSION")
	PSESSION = getenv("PSESSION")
	LOG_CHANNEL = getenv("LOG_CHANNEL")

	
	