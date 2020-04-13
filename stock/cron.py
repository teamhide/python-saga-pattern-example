import pika
from model import Stock
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
        order_id, item_id = body.decode('utf8').split(':')  # order_id:item_id
        stock = session.query(Stock).filter(Stock.item_id == item_id).first()
        stock.count = Stock.count - 1
        session.add(stock)
        session.commit()

        self.produce(exchange='', routing_key='stock_success', body=order_id)
        print(f'[*] Produce to `stock_success` -> `{order_id}`')

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
        self.queue.consume(queue='order_created')


if __name__ == '__main__':
    cron = Cron(queue=MQ(
        id='admin',
        password='admin',
        host='mq',
        port=5672,
    ))
    cron.run()
