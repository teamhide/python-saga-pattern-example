from fastapi import FastAPI, Request

from .db import session, Base, engine
from .model import Order
from .message_queue import MQ

app = FastAPI()


@app.middleware('http')
async def remove_session(request: Request, call_next):
    response = await call_next(request)
    session.remove()
    return response


@app.get('/order/{item_id}')
async def create_order(item_id: int):
    order = Order(item_id=item_id, status='pending')
    session.add(order)
    session.commit()

    mq = MQ(
        id='admin',
        password='admin',
        host='mq',
        port=5672,
    )
    mq.produce(
        exchange='',
        routing_key='order_created',
        body=f'{order.id}:{item_id}',
    )
    mq.consume(queue='delivery_success')
    mq.close()
    return {'status': True}
