from fastapi import FastAPI, Request

from .db import session, Base, engine
from .message_queue import Producer
from .model import Order

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

    producer = Producer(
        id='admin',
        password='admin',
        host='localhost',
        port=5672,
        queue='order',
    )
    producer.produce(
        exchange='',
        routing_key='ORDER_CREATED',
        body=f'{order.id}:{item_id}',
    )
