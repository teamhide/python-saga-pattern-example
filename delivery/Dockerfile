FROM python:3.8.1
MAINTAINER hide <padocon@naver.com>

COPY . /home
RUN pip3 install gunicorn
RUN pip3 install pika
WORKDIR /home
RUN sleep 5

CMD python3 payment/cron.py