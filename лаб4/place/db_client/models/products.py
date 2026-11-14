from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship

from .base import Base


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, default=0)
    quantity = Column(Integer, nullable=False)
    store_id = Column(Integer, ForeignKey('stores.store_id'), nullable=False)

    store = relationship("Store", back_populates="products")
    order_items = relationship("OrderProduct", back_populates="product", cascade="all, delete-orphan")
    carts = relationship("Cart", back_populates="products", cascade="all, delete-orphan")
    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        UniqueConstraint('product_id', 'customer_id', name='unique_product_customer'),
    )

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Integer, nullable=False)
    comment = Column(Text)
    date = Column(Date, nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)

    product = relationship("Product", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")
