
FROM python:3

ENV TZ=America/New_York
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /usr/src/app

COPY RedditPostNotification.py .
COPY config.json .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install praw

CMD [ "python3", "RedditPostNotification.py" ]
