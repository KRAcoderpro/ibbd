from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    status = Column(String(100), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")


class OrderProduct(Base):
    __tablename__ = 'orders_products'

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    status = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

