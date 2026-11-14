import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from . import models
from .errors import product_errors, DBError
from .base_db_client import BaseDBClient


class ProductsDBClient:
    def __init__(self, db_client: BaseDBClient):
        self._db_client = db_client
        self._db: Session = self._db_client.get_db()

    def add_product(
        self,
        name: str,
        description: str,
        price: int,
        discount: int,
        quantity: int,
        store_id: int
    ) -> None:
        new_product = models.Product(
            name=name,
            description=description,
            price=price,
            discount=discount,
            quantity=quantity,
            store_id=store_id
        )
        try:
            self._db.add(new_product)
            self._db.commit()
            self._db.refresh(new_product)
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def update_product(
        self,
        product_id,
        name: str,
        description: str,
        price: int,
        discount: int,
        quantity: int,
    ) -> None:
        product = self._db.query(models.Product).filter(
            models.Product.product_id == product_id).first()

        if product is None:
            raise product_errors.ProductNotFoundError()

        product.name = name
        product.description = description
        product.price = price
        product.discount = discount
        product.quantity = quantity

        try:
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def delete_product_by_id(self, product_id: int) -> None:
        product = self._db.query(models.Product).filter(
            models.Product.product_id == product_id).first()

        if product is None:
            raise product_errors.ProductNotFoundError()

        try:
            self._db.delete(product)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def add_product_review(
            self,
            grade: int,
            comment: str,
            date: datetime.datetime,
            product_id: int,
            customer_id: int
    ) -> None:
        new_product_review = models.Review(
            grade=grade,
            comment=comment,
            date=date,
            product_id=product_id,
            customer_id=customer_id
        )
        try:
            self._db.add(new_product_review)
            self._db.commit()
            self._db.refresh(new_product_review)
        except Exception as exc:
            self._db.rollback()
            print(str(exc))
            raise DBError() from exc

    def get_product_reviews(self, product_id: int) -> list[dict]:
        # Выполняем запрос с агрегированием данных по отзывам
        product_reviews = self._db.query(
            models.ProductReviews.product_id,
            models.ProductReviews.customer_id,
            models.ProductReviews.rating,
            models.ProductReviews.review_comment,
            models.ProductReviews.customer_name,
            models.ProductReviews.review_date
        ).filter(
            models.ProductReviews.product_id == product_id
        ).order_by(
            desc(models.ProductReviews.review_date)  # Сортировка по дате отзыва
        ).all()

        # Преобразуем результаты в формат списка словарей
        return [
            {
                "product_id": review.product_id,
                "customer_id": review.customer_id,
                "rating": review.rating,
                "review_comment": review.review_comment,
                "customer_name": review.customer_name,
                "review_date": review.review_date
            }
            for review in product_reviews
        ]

    def get_all_products(self) -> list[dict]:
        db_products = self._db.query(models.Product).all()

        return [
            product.__dict__
            for product in db_products
        ]

    def get_product(self, product_id: int,) -> dict:
        product = self._db.query(models.Product).filter(
            models.Product.product_id == product_id).first()

        if product is None:
            raise product_errors.ProductNotFoundError()

        return product.__dict__

    def decrease_product_quantity(self, product_id: int, quantity: int) -> None:
        product = self._db.query(models.Product).filter(
            models.Product.product_id == product_id).first()

        if product is None:
            raise product_errors.ProductNotFoundError()

        if product.quantity == 0:
            return

        product.quantity -= quantity if product.quantity > quantity else product.quantity

        try:
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def get_store_products(self, store_id: int) -> list[dict]:
        # Выполняем запрос с агрегированием данных по отзывам
        store_product_catalog = self._db.query(
            models.StoreProductCatalog.product_id,
            models.StoreProductCatalog.store_id,
            models.StoreProductCatalog.product_name,
            models.StoreProductCatalog.product_price,
            models.StoreProductCatalog.product_discount,
            models.StoreProductCatalog.average_rating,
            models.StoreProductCatalog.product_quantity,

        ).filter(
            models.StoreProductCatalog.store_id == store_id
        ).order_by(
            models.StoreProductCatalog.product_id  # Сортировка по дате отзыва
        ).all()

        return [
            {
                "product_id": product.product_id,
                "store_id": product.store_id,
                "product_name": product.product_name,
                "product_price": product.product_price,
                "product_discount": product.product_discount,
                "average_rating": round(product.average_rating),
                "product_quantity": product.product_quantity
            }
            for product in store_product_catalog
        ]



