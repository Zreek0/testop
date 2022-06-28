import glob, logging, asyncio
from pathlib import Path
from .loader import load_plugins
from . import bot, client

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

path = "./main/plugins/*py"
files = glob.glob(path)
for name in files:
	with open(name) as f:
		p = Path(f.name)
		plugin_name = p.stem
		load_plugins(plugin_name.replace(".py", ""))
logging.getLogger(__name__).info("✦ Successfully Deployed Bot")
if __name__ == "__main__":
	client.start()
	client.tgbot
	client.run_until_disconected()
