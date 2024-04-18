FROM ubuntu:latest
LABEL maintainer="Cécile,Jynaldo,Yoan,Alice"

RUN apt update && \
    apt-get install -y zip && \
    apt-get install -y vim && \
    apt-get install -y python3.10 && \
    apt-get install -y python3-pip

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

WORKDIR /app/web_app

#CMD ["python3", "app.py"]

