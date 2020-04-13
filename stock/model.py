from sqlalchemy import Column, BigInteger, func, DateTime, Integer

from db import Base


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item_id = Column(BigInteger, nullable=False)
    count = Column(Integer, default=100)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
