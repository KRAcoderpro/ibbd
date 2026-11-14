from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Seller(Base):
    __tablename__ = 'sellers'
    __table_args__ = (
        UniqueConstraint('inn', name='unique_seller_inn'),
        UniqueConstraint('phone', name='unique_seller_phone'),
        UniqueConstraint('email', name='unique_seller_email'),
    )

    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    inn = Column(String(12), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)

    # Связь с таблицей Store
    store = relationship("Store", back_populates="seller", cascade="all, delete-orphan")


class Store(Base):
    __tablename__ = 'stores'
    __table_args__ = (
        UniqueConstraint('name', name='unique_stores_name'),
        UniqueConstraint('seller_id', name='unique_stores_seller'),
    )

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'), nullable=False)

    # Связь с таблицей Seller
    seller = relationship("Seller", back_populates="store")

    products = relationship("Product", back_populates="store",
                            cascade="all, delete-orphan")
