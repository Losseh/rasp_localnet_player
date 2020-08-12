FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev mplayer

RUN pip install flask

RUN mkdir -p /home/pi/player
COPY player /home/pi/player

ENTRYPOINT ["python", "/home/pi/player/main.py"]
