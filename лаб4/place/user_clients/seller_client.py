import re

from sqlalchemy.orm import Session

from db_client import SellerDBClient, OrdersDBClient, BaseDBClient, structures, ProductsDBClient


class SellersClient:
    def __init__(self, db_client: BaseDBClient):
        self._sellers_db_client = SellerDBClient(db_client)
        self._products_db_client = ProductsDBClient(db_client)

    def add_product(
            self,
            name: str,
            description: str,
            price: int,
            discount: int,
            quantity: int,
            store_id: int
    ) -> None:

        self._products_db_client.add_product(
            name,
            description,
            price,
            discount,
            quantity,
            store_id
        )

    def get_product(
            self, product_id: int
    ) -> dict:

        return self._products_db_client.get_product(product_id)

    def update_product(
            self,
            product_id,
            name: str,
            description: str,
            price: int,
            discount: int,
            quantity: int,
    ) -> None:

        self._products_db_client.update_product(
            product_id,
            name,
            description,
            price,
            discount,
            quantity,
        )

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
    
    @staticmethod
    def validate_phone(phone_number: str) -> str:
        validated = re.sub(r"[^\d]+", "", phone_number)

        validated = f"+{validated}" if not validated.startswith("+") else validated

        print(validated)

        return validated
