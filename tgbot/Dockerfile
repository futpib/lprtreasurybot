 
FROM python:latest

LABEL MAINTAINER="dkeysil dkeysil@protonmail.com"

WORKDIR /treasurybot
ADD ./requirements.txt /treasurybot/requirements.txt
RUN pip install -r requirements.txt
ADD . /treasurybot

CMD python -u __main__.py
