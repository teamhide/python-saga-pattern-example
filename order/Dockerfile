FROM python:3.8.1
MAINTAINER hide <padocon@naver.com>

COPY . /home
RUN pip3 install fastapi
RUN pip3 install sqlalchemy
RUN pip3 install uvicorn
RUN pip3 install pymysql
RUN pip3 install pika
WORKDIR /home

CMD python3 order/main.py