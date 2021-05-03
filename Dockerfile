FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y

ENV TZ=America/New_York

WORKDIR /usr/src/app

# copy the required files to the working directory
COPY src/redditPostNotification.py .
COPY config.json .
COPY requirements.txt .

# install python3 and pip
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN python3 -m pip install --upgrade pip

# install required packages
RUN pip3 install -r requirements.txt

# install sqlite3
RUN apt-get install sqlite3 -y

CMD [ "python3", "reddit_post_notification.py" ]
