import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from . import models
from .errors import order_errors, DBError
from .base_db_client import BaseDBClient


class OrdersDBClient:
    def __init__(self, db_client: BaseDBClient):
        self._db_client = db_client
        self._db: Session = self._db_client.get_db()

    def add_order(
            self, date: datetime.datetime, status: str, customer_id: int
    ) -> int:

        new_order = models.Order(
            date=date,
            status=status,
            customer_id=customer_id
        )
        try:
            self._db.add(new_order)
            self._db.commit()
            self._db.refresh(new_order)
            return new_order.order_id
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def add_product_to_order(
            self, product_id: int, order_id: int, quantity: int, status: str
    ) -> None:

        new_product_to_order = models.OrderProduct(
            product_id=product_id,
            order_id=order_id,
            quantity=quantity,
            status=status
        )
        try:
            self._db.add(new_product_to_order)
            self._db.commit()
            self._db.refresh(new_product_to_order)
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def delete_order_by_id(self, order_id: int) -> None:
        order = self._db.query(models.Order).filter(
            models.Order.order_id == order_id).first()
        if order is None:
            raise order_errors.OrderNotFoundError()

        try:
            self._db.delete(order)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def delete_product_from_order(self, product_id: int, order_id: int) -> None:
        order = self._db.query(models.Order).filter(
            models.Order.order_id == order_id).first()
        if order is None:
            raise order_errors.OrderNotFoundError()

        order_in_product = self._db.query(models.OrderProduct).filter(
            models.OrderProduct.order_id == order_id,
            models.OrderProduct.product_id == product_id
        ).first()

        try:
            self._db.delete(order_in_product)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def get_orders(self, customer_id: int) -> list[dict]:
        customer_order_details = self._db.query(
            models.CustomersOrderDetails.order_id,
            func.max(models.CustomersOrderDetails.order_date).label("order_date"),
            func.max(models.CustomersOrderDetails.order_status).label("order_status"),
            func.array_agg(models.CustomersOrderDetails.product_id).label(
                "product_ids"),
            func.array_agg(models.CustomersOrderDetails.product_name).label(
                "product_names"),
            func.array_agg(models.CustomersOrderDetails.product_quantity).label(
                "product_quantities"),
            func.array_agg(models.CustomersOrderDetails.product_status).label(
                "product_statuses")
        ).filter(
            models.CustomersOrderDetails.customer_id == customer_id
        ).group_by(
            models.CustomersOrderDetails.order_id
        ).order_by(
            desc(func.max(models.CustomersOrderDetails.order_id))
        ).all()

        # Преобразование результатов в список словарей
        return [
            {
                "order_id": row.order_id,
                "order_date": row.order_date,
                "order_status": row.order_status,
                "products": [
                    {
                        "product_id": product_id,
                        "product_name": product_name,
                        "product_quantity": product_quantity,
                        "product_status": product_status,
                    }
                    for product_id, product_name, product_quantity, product_status in
                    zip(
                        row.product_ids, row.product_names, row.product_quantities,
                        row.product_statuses
                    )
                ]
            }
            for row in customer_order_details
        ]

    def get_store_orders(self, store_id: int) -> list[dict]:
        # Выполняем запрос с агрегированием данных по отзывам
        seller_all_orders = self._db.query(
            models.SellerAllOrders.product_id,
            models.SellerAllOrders.store_id,
            models.SellerAllOrders.order_id,
            models.SellerAllOrders.product_name,
            models.SellerAllOrders.order_date,
            models.SellerAllOrders.order_status,
            models.SellerAllOrders.product_quantity,

        ).filter(
            models.SellerAllOrders.store_id == store_id
        ).order_by(
            desc(models.SellerAllOrders.order_date)
        ).all()

        return [
            {
                "product_id": order.product_id,
                "store_id": order.store_id,
                "order_id": order.order_id,
                "product_name": order.product_name,
                "order_date": order.order_date,
                "order_status": order.order_status,
                "product_quantity": order.product_quantity
            }
            for order in seller_all_orders
        ]
