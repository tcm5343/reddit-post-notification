FROM python:3

ENV TZ=America/New_York
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /usr/src/app

COPY redditPostNotification.py .
COPY config.json .
COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "redditPostNotification.py" ]
