import datetime
import re

from sqlalchemy.orm import Session

from db_client import CustomersDBClient, OrdersDBClient, BaseDBClient, structures, ProductsDBClient


class CustomersClient:
    def __init__(self, db_client: BaseDBClient):
        self._customer_db_client = CustomersDBClient(db_client)
        self._orders_db_client = OrdersDBClient(db_client)
        self._products_db_client = ProductsDBClient(db_client)

    def add_customer(
            self, name: str, phone: str
    ) -> int:
        phone = self.validate_phone(phone)

        customer_id = self._customer_db_client.add_customer(name, phone)
        
        return customer_id

    def get_customer(
            self, customer_id: int
    ) -> structures.Customer | None:

        return self._customer_db_client.get_customer(customer_id)

    def get_customer_by_phone(
            self, phone: str
    ) -> structures.Customer | None:
        return self._customer_db_client.get_customer_by_phone(phone)

    def delete_customer(self, customer_id: int) -> None:
        self._customer_db_client.delete_customer(customer_id)

    def get_cart(
        self, customer_id: int
    ) -> list[dict]:

        return self._customer_db_client.get_cart(customer_id)

    def add_to_cart(
            self, customer_id: int, product_id: int, quantity: int
    ) -> None:

        self._customer_db_client.add_to_cart(customer_id, product_id, quantity)

    def remove_from_cart(self, customer_id: int, product_id: int) -> None:

        self._customer_db_client.remove_from_cart(customer_id, product_id)

    def delete_from_cart(
        self, customer_id: int, product_id: int
    ) -> None:

        self._customer_db_client.delete_from_cart(customer_id, product_id)

    def get_orders(self, customer_id: int) -> list[dict]:
        return self._orders_db_client.get_orders(customer_id=customer_id)

    def create_order(self, customer_id: int):
        products = self._customer_db_client.get_cart(
            customer_id=customer_id)

        if not products:
            raise

        order_id = self._orders_db_client.add_order(
            date=datetime.datetime.now(),
            status="accepted",
            customer_id=customer_id
        )

        for product in products:
            products_left = self._products_db_client.get_product(
                product["product_id"]
            )["quantity"]

            if products_left == 0:
                break

            self._orders_db_client.add_product_to_order(
                product_id=product["product_id"],
                order_id=order_id,
                quantity=product["quantity"] if product[
                                                    "quantity"] < products_left else products_left,
                status="accepted"
            )

            self._products_db_client.decrease_product_quantity(
                product_id=product["product_id"],
                quantity=product["quantity"]
            )

            self._customer_db_client.delete_from_cart(
                customer_id=customer_id, product_id=product["product_id"]
            )

    def add_product_review(
            self,
            grade: int,
            comment: str,
            date: datetime.datetime,
            product_id: int,
            customer_id: int
    ):
        self._products_db_client.add_product_review(
            grade,
            comment,
            date,
            product_id,
            customer_id
        )

    @staticmethod
    def validate_phone(phone_number: str) -> str:
        validated = re.sub(r"[^\d]+", "", phone_number)

        validated = f"+{validated}" if not validated.startswith("+") else validated

        print(validated)

        return validated
