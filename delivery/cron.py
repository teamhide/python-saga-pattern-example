import pika
from model import Delivery
from db import session


class MQ:
    def __init__(
        self,
        id: str,
        password: str,
        host: str,
        port: int,
    ):
        self.conn = pika.BlockingConnection(
            pika.URLParameters(f'amqp://{id}:{password}@{host}:{port}'),
        )
        self.channel = self.conn.channel()
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue='order_created')
        self.channel.queue_declare(queue='stock_success')
        self.channel.queue_declare(queue='delivery_success')
        self.channel.queue_declare(queue='stock_fail')
        self.channel.queue_declare(queue='delivery_fail')

    def callback(self, ch, method, properties, body: bytes) -> None:
        order_id = body.decode('utf8')
        delivery = Delivery(order_id=order_id)
        session.add(delivery)
        session.commit()

        self.produce(exchange='', routing_key='delivery_success', body=order_id)
        print(f'[*] Produce to `delivery_success` -> `{order_id}`')

    def consume(self, queue: str) -> None:
        self.channel.basic_consume(
            on_message_callback=self.callback,
            queue=queue,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def produce(self, exchange: str, routing_key: str, body: str) -> None:
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
        )

    def close(self):
        self.conn.close()


class Cron:
    def __init__(self, queue: MQ):
        self.queue = queue

    def run(self):
        self.queue.consume(queue='stock_success')


if __name__ == '__main__':
    cron = Cron(queue=MQ(
        id='admin',
        password='admin',
        host='mq',
        port=5672,
    ))
    cron.run()
