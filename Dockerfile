FROM python:3.12

WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app/src
ENV PYTHONUNBUFFERED=1

COPY . .
RUN chmod +x do/lint.sh do/test.sh

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./src/reddit_post_notification/reddit_post_notification.py" ]

# FROM ubuntu:24.10

# RUN apt-get update -y
# RUN apt-get install sqlite3 -y

#WORKDIR /usr/src/app
#ENV PYTHONPATH=/usr/src/app/src
#
#ENV TZ=America/New_York
#ENV PYTHONUNBUFFERED=1
#
#COPY src ./src
#COPY config.json .
#COPY requirements.txt .
#
## python3
#RUN apt-get install python3 -y
#RUN apt-get install python3-pip -y
#RUN apt-get install python3.12-venv -y
#
#RUN python3 -m venv .venv
## RUN python3 -m pip install --upgrade pip
#
#RUN .venv/bin/pip3 install -r requirements.txt
#
#CMD [ ".venv/bin/python3", "src/reddit_post_notification/reddit_post_notification.py" ]
