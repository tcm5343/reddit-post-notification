FROM python:3

ENV TZ=America/New_York
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /usr/src/app

COPY RedditPostNotification.py .
COPY config.json .

RUN pip3 install praw

CMD [ "python", "./RedditPostNotification.py" ]
