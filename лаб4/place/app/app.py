from fastapi import FastAPI, HTTPException, Request
from . import dependacy
from fastapi.responses import RedirectResponse
from db_client import SellerDBClient, CustomersDBClient, ProductsDBClient, OrdersDBClient
from auth import JWTEncryption
from user_clients import CustomersClient, SellersClient
from . import schemas


def create_app(
        sellers_db_client: SellerDBClient,
        customers_db_client: CustomersDBClient,
        products_db_client: ProductsDBClient,
        orders_db_client: OrdersDBClient,
        jwt_encryption: JWTEncryption,

) -> FastAPI:
    dependacy.seller_db_client = sellers_db_client
    dependacy.customers_db_client = customers_db_client
    dependacy.products_db_client = products_db_client
    dependacy.orders_db_client = orders_db_client
    dependacy.jwt_encryption = jwt_encryption


    from . import routes

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )

    @app.exception_handler(schemas.response.error.TokenVerificationFailedException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/customers/login", status_code=303)

    @app.exception_handler(schemas.response.error.TokenExpiredException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/customers/login", status_code=303)

    @app.exception_handler(schemas.response.error.TokenNotFoundException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/customers/login", status_code=303)

    @app.exception_handler(schemas.response.error.AccessTokenException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/customers/login", status_code=303)

    @app.exception_handler(schemas.response.error.SellerTokenVerificationFailedException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/sellers/login", status_code=303)

    @app.exception_handler(schemas.response.error.SellerTokenExpiredException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/sellers/login", status_code=303)

    @app.exception_handler(schemas.response.error.SellerTokenNotFoundException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/sellers/login", status_code=303)

    @app.exception_handler(schemas.response.error.SellerTokenException)
    async def unauthorized_exception_handler(response: Request, exc: HTTPException):
        return RedirectResponse(url="/sellers/login", status_code=303)

    app.include_router(routes.seller_router)
    app.include_router(routes.customers_router)
    app.include_router(routes.products_router)
    app.include_router(routes.orders_router)
    app.include_router(routes.view_router)

    return app
