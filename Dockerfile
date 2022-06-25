FROM python

RUN apt update -y && apt upgrade -y
RUN sudo apt install -y --no-install-recommends ffmpeg python3 python3-pip mediainfo python3-selenium chromium-driver 
RUN pip install --no-cache-dir -r requirements.txt

CMD python -m main
