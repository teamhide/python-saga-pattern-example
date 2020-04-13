# Python SAGA Pattern Example

Implemented SAGA Pattern through python for distributed transaction.

- FastAPI
- RabbitMQ


There is three microsevices.
- Order
- Stock
- Delivery

Each service is listening to a specific queue, as shown below.
- ORDER_CREATED: order
- STOCK_SUCCESS: delivery
- DELIVERY_SUCCESS: order
- STOCK_FAIL: order
- DELIVERY_FAIL: order, stock