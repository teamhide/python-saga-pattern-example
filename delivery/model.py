from sqlalchemy import Column, BigInteger, func, DateTime

from db import Base


class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
