FROM python:3.8.1
MAINTAINER hide <padocon@naver.com>

COPY . /home
RUN pip3 install gunicorn
RUN pip3 install pika
WORKDIR /home
RUN apt-get update && apt-get install -y netcat
RUN chmod +x stock/wait.sh

CMD stock/wait.sh