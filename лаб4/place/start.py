from db_client import BaseDBClient, SellerDBClient, CustomersDBClient, ProductsDBClient, OrdersDBClient
from user_clients import CustomersClient, SellersClient
from auth import JWTEncryption
from app import create_app
import environment as env
import uvicorn


def main():
    db_client = BaseDBClient(db_url=env.DB_URL)
    seller_db_client = SellerDBClient(db_client=db_client)
    customers_sb_client = CustomersDBClient(db_client=db_client)
    products_db_client = ProductsDBClient(db_client=db_client)
    orders_db_client = OrdersDBClient(db_client=db_client)
    jwt_encryption = JWTEncryption("secret", "HS256", 30)

    web_app = create_app(
        sellers_db_client=seller_db_client,
        customers_db_client=customers_sb_client,
        products_db_client=products_db_client,
        orders_db_client=orders_db_client,
        jwt_encryption=jwt_encryption,

    )

    uvicorn.run(web_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
