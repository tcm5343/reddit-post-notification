FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y

ENV TZ=America/New_York

WORKDIR /usr/src/app

COPY redditPostNotification.py .
COPY config.json .
COPY requirements.txt .

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get install sqlite3 -y

CMD [ "python3", "redditPostNotification.py" ]
