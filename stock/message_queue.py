import pika
from model import Stock
from db import session


class Producer:
    def __init__(
        self,
        id: str,
        password: str,
        host: str,
        port: str,
        queue: str,
    ):
        self.conn = pika.BlockingConnection(
            pika.URLParameters(f'amqp://{id}:{password}@{host}:{port}'),
        )
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=queue)

    def produce(self, exchange: str, routing_key: str, body: str) -> None:
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
        )
        self.conn.close()


class Consumer:
    def __init__(
        self,
        id: str,
        password: str,
        host: str,
        port: int,
        queue: str,
    ):
        self.queue = queue
        self.conn = pika.BlockingConnection(
            pika.URLParameters(f'amqp://{id}:{password}@{host}:{port}'),
        )
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=self.queue)

    def callback(self, ch, method, properties, body: bytes) -> None:
        stock = Stock()
        session.add(stock)
        session.commit()
        print(" [x] Received %r" % body.decode('utf8'))

    def consume(self) -> None:
        self.channel.basic_consume(
            on_message_callback=self.callback,
            queue=self.queue,
            auto_ack=True,
        )
        self.channel.start_consuming()
