from fastapi import Request

from .. import dependacy
from .. import schemas
from auth import errors as auth_errors


def get_current_user(
        request: Request
) -> schemas.response.custoemrs.Customer:
    token = request.cookies.get("access_token")

    if token is None:
        raise schemas.response.error.TokenNotFoundException()

    try:
        payload = dependacy.jwt_encryption.verify_jwt_token(token)
    except auth_errors.TokenExpiredError:
        raise schemas.response.error.TokenExpiredException()
    except auth_errors.TokenVerificationError:
        raise schemas.response.error.TokenVerificationFailedException()

    customer_id = payload.get("customer_id")

    if customer_id is None:
        raise schemas.response.error.AccessTokenException() from None

    customer = dependacy.customers_db_client.get_customer(
        customer_id=customer_id
    )

    if customer is None:
        raise schemas.response.error.AccessTokenException()

    return schemas.response.custoemrs.Customer(
        customer_id=customer_id,
        name=customer.name
    )


def get_current_seller(
        request: Request
) -> schemas.response.sellers.Seller:
    token = request.cookies.get("seller_token")

    if token is None:
        raise schemas.response.error.SellerTokenNotFoundException()

    try:
        payload = dependacy.jwt_encryption.verify_jwt_token(token)
    except auth_errors.TokenExpiredError:
        raise schemas.response.error.SellerTokenExpiredException()
    except auth_errors.TokenVerificationError:
        raise schemas.response.error.SellerTokenVerificationFailedException()

    phone = payload.get("phone")

    if phone is None:
        raise schemas.response.error.SellerTokenException() from None

    seller = dependacy.seller_db_client.get_seller_by_phone(
        phone=phone
    )

    if seller is None:
        raise schemas.response.error.SellerTokenException()

    return schemas.response.sellers.Seller(
        phone=seller.phone,
        store_id=seller.store_id
    )
