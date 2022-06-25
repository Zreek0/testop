from os import getenv
from dotenv import load_dotenv, find_dotenv, dotenv_values

try:
    load_dotenv(find_dotenv())
except:
    raise
Config = dotenv_values(find_dotenv())


	
	
