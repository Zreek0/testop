from os import environ
from dotenv import load_dotenv, find_dotenv, dotenv_values

try:
    load_dotenv(find_dotenv())
except:
    raise
Config = environ


	
	
