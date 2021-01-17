FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
COPY RedditPostNotification.py .
COPY config.json .

RUN pip3 install praw

CMD [ "python", "./RedditPostNotification.py" ]
