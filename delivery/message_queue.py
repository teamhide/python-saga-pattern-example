import pika


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
        self.conn = pika.BlockingConnection(
            pika.URLParameters(f'amqp://{id}:{password}@{host}:{port}'),
        )
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=queue)

    def callback(self, ch, method, properties, body: str) -> None:
        print(" [x] Received %r" % body)

    def consume(self, queue: str) -> None:
        self.channel.basic_consume(
            on_message_callback=self.callback,
            queue=queue,
            auto_ack=True,
        )
        self.channel.start_consuming()
