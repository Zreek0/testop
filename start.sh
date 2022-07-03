cd /
rm -rf testbot
git clone -b main https://github.com/Zreek0/testop testbot
cd testbot
pip install --quiet --requirements requirements.txt
python3 -m main
