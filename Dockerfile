FROM ubuntu:20.04

ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y && apt upgrade -y
RUN apt install -y --no-install-recommends python3 python3-pip python3-selenium chromium-driver

RUN git clone https://github.com/Zreek0/testop testbot
WORKDIR testbot
RUN pip install --no-cache-dir -r requirements.txt



CMD bash start.sh
