import glob, logging, asyncio
from pathlib import Path
from .loader import load_plugins
from . import bot

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)

path = "./main/plugins/*py"
files = glob.glob(path)
for name in files:
	with open(name) as f:
		p = Path(f.name)
		plugin_name = p.stem
		load_plugins(plugin_name.replace(".py", ""))
try:
    asyncio.run(bot.disconnect())
excep Exception as e:
    print(str(e))
print("• Successfully Deployed Bot")
if __name__ == "__main__":
        bot = bot.start(bot_token=Config.get("BOT_TOKEN")
	bot.run_until_disconnected()
