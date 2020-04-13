from message_queue import Producer, Consumer
from db import Payment


class Cron:
    def __init__(self, producer: Producer, consumer: Consumer):
        self.producer = producer
        self.consumer = consumer

    def run(self):
        pass


if __name__ == '__main__':
    producer = Producer(
        id='admin',
        password='admin',
        host='localhost',
        port=5672,
        queue='order',
    )
    consumer = Consumer(
        id='admin',
        password='admin',
        host='localhost',
        port=5672,
        queue='order',
    )
    cron = Cron(producer=producer, consumer=consumer)
