FROM ubuntu:latest

COPY . /data
WORKDIR /data

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt

CMD [ "/usr/bin/python3", "DockerChannel.py" ]
