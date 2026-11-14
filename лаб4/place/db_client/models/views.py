from sqlalchemy import Column, Integer, Text, Date, Numeric

from .base import Base


class CustomersOrderDetails(Base):
    __tablename__ = 'customer_order_details'  # Имя представления
    __table_args__ = {'extend_existing': True}

    order_id = Column(Integer, primary_key=True, autoincrement=False)
    customer_id = Column(Integer)
    order_date = Column(Date)
    order_status = Column(Text)
    product_id = Column(Integer, primary_key=True, autoincrement=False)
    product_name = Column(Text)
    product_quantity = Column(Text)
    product_status = Column(Text)


class ProductReviews(Base):
    __tablename__ = 'product_reviews'  # Имя представления
    __table_args__ = {'extend_existing': True}

    product_id = Column(Integer, primary_key=True, autoincrement=False)
    customer_id = Column(Integer, primary_key=True, autoincrement=False)
    rating = Column(Integer)
    review_date = Column(Date)
    review_comment = Column(Text)
    customer_name = Column(Text)


class StoreProductCatalog(Base):
    __tablename__ = 'store_product_catalog'  # Имя представления
    __table_args__ = {'extend_existing': True}

    store_id = Column(Integer, primary_key=True, autoincrement=False)
    product_id = Column(Integer, primary_key=True, autoincrement=False)
    product_name = Column(Text)
    product_price = Column(Integer)
    product_discount = Column(Integer)
    average_rating = Column(Numeric)
    product_quantity = Column(Integer)


class SellerAllOrders(Base):
    __tablename__ = 'seller_all_orders'  # Имя представления
    __table_args__ = {'extend_existing': True}

    store_id = Column(Integer, primary_key=True, autoincrement=False)
    product_id = Column(Integer, primary_key=True, autoincrement=False)
    order_id = Column(Integer, primary_key=True, autoincrement=False)
    order_date = Column(Date)
    product_name = Column(Text)
    order_status = Column(Text)
    product_quantity = Column(Integer)


