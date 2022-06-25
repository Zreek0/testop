FROM python

COPY requirements.txt .
RUN apt update -y && apt upgrade -y
RUN apt install -y --no-install-recommends ffmpeg python3 python3-pip mediainfo python3-selenium chromium-driver 
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /root/testop

CMD python -m main
