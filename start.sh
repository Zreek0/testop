cd /
rm -rf userbot
git clone https://github.com/Zreek0/testop userbot
cd userbot
pip install --quiet -r requirements.txt
python3 -m main
