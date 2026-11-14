from sqlalchemy.orm import Session

from . import models, structures
from .errors import customer_errors, DBError
from .base_db_client import BaseDBClient


class CustomersDBClient:
    def __init__(self, db_client: BaseDBClient):
        self._db_client = db_client
        self._db: Session = self._db_client.get_db()

    def add_customer(
            self, name: str, phone: str
    ) -> int:
        phone = self._db_client.validate_phone(phone)

        db_customer = self._db.query(models.Customer).filter(
            models.Customer.phone == phone).first()
        if db_customer:
            raise customer_errors.CustomerAlreadyExistsError()

        new_customer = models.Customer(
            name=name,
            phone=phone,
        )
        try:
            self._db.add(new_customer)
            self._db.commit()
            self._db.refresh(new_customer)
            return new_customer.customer_id
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def get_customer(
            self, customer_id: int
    ) -> structures.Customer | None:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if db_customer is None:
            return None

        return structures.Customer(**db_customer.__dict__)

    def get_customer_by_phone(
            self, phone: str
    ) -> structures.Customer | None:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.phone == phone).first()

        if db_customer is None:
            return None

        return structures.Customer(**db_customer.__dict__)

    def delete_customer(self, customer_id: int) -> None:
        customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if customer is None:
            raise customer_errors.CustomerNotFoundError()

        try:
            self._db.delete(customer)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def get_cart(
        self, customer_id: int
    ) -> list[dict]:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if db_customer is None:
            raise customer_errors.CustomerNotFoundError()

        cart = self._db.query(models.Cart).join(models.Product).filter(
            models.Cart.customer_id == customer_id
        ).order_by(models.Product.name).all()

        products = []
        for cart_product in cart:
            if cart_product.products.quantity == 0:
                self.remove_from_cart(customer_id, cart_product.product_id)
                return products

            product = cart_product.products.__dict__
            product.update({"quantity": cart_product.quantity})
            products.append(product)

        return products

    def add_to_cart(
            self, customer_id: int, product_id: int, quantity: int
    ) -> None:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if db_customer is None:
            raise customer_errors.CustomerNotFoundError()

        product_cart = self._db.query(models.Cart).filter(
            models.Cart.product_id == product_id,
            models.Cart.customer_id == db_customer.customer_id
        ).first()

        if product_cart:
            if product_cart.products.quantity == 0:
                raise customer_errors.NoProductsLeft()

            product_cart.quantity += quantity
            try:
                self._db.commit()
            except Exception as exc:
                self._db.rollback()
                raise DBError() from exc

            return

        new_product_cart = models.Cart(
            customer_id=db_customer.customer_id,
            product_id=product_id,
            quantity=quantity
        )
        try:
            self._db.add(new_product_cart)
            self._db.commit()
            self._db.refresh(new_product_cart)
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def remove_from_cart(self, customer_id: int, product_id: int) -> None:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if db_customer is None:
            raise customer_errors.CustomerNotFoundError()

        product_cart = self._db.query(models.Cart).filter(
            models.Cart.product_id == product_id,
            models.Cart.customer_id == db_customer.customer_id
        ).first()

        if product_cart is None:
            raise customer_errors.NoProductInCart()

        if product_cart.quantity != 0:
            product_cart.quantity -= 1
        else:
            self.delete_from_cart(customer_id, product_id)
        try:
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

        return

    def delete_from_cart(
        self, customer_id: int, product_id: int
    ) -> None:
        db_customer = self._db.query(models.Customer).filter(
            models.Customer.customer_id == customer_id).first()

        if db_customer is None:
            raise customer_errors.CustomerNotFoundError()

        product_cart = self._db.query(models.Cart).filter(
            models.Cart.product_id == product_id,
            models.Cart.customer_id == db_customer.customer_id
        ).first()

        if product_cart is None:
            raise customer_errors.NoProductInCart()

        try:
            self._db.delete(product_cart)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

        return
