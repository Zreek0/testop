FROM python

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Asia/Kolkata

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 
RUN apt update -y && apt upgrade -y
RUN sudo apt install -y --no-install-recommends ffmpeg python3 python3-pip mediainfo python3-selenium chromium-driver 
RUN pip install --no-cache-dir -r requirements.txt

CMD python -m main
