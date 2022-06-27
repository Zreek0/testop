FROM python

COPY . .

ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -y && apt upgrade -y
RUN apt install -y --no-install-recommends ffmpeg python3 python3-pip python3-selenium chromium-driver 
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR .

CMD python -m main
