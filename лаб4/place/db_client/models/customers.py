from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        UniqueConstraint('phone', name='customers_unique'),
    )

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)

    reviews = relationship("Review", back_populates="customer",
                           cascade="all, delete-orphan")

    orders = relationship("Order", back_populates="customer",
                          cascade="all, delete-orphan")

    carts = relationship("Cart", back_populates="customers", cascade="all, delete-orphan")


class Cart(Base):
    __tablename__ = 'carts'

    customer_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    customers = relationship("Customer", back_populates="carts")
    products = relationship("Product", back_populates="carts")
