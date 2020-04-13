from message_queue import Producer, Consumer


class Cron:
    def __init__(self, producer: Producer, consumer: Consumer):
        self.producer = producer
        self.consumer = consumer

    def run(self):
        self.consumer.consume(queue='ORDER_CREATED')


if __name__ == '__main__':
    from time import sleep
    sleep(5)
    producer = Producer(
        id='admin',
        password='admin',
        host='mq',
        port=5672,
        queue='order',
    )
    consumer = Consumer(
        id='admin',
        password='admin',
        host='mq',
        port=5672,
        queue='order',
    )
    cron = Cron(producer=producer, consumer=consumer)
    cron.run()
