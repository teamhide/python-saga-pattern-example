from sqlalchemy import Column, BigInteger, Unicode, DateTime, func

from .db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item_id = Column(BigInteger, nullable=False)
    status = Column(Unicode(255), default='pending')
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
