import datetime
import functools
from datetime import timedelta

from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
import logging
from typing import TypeVar, ParamSpec, Callable
from fastapi.templating import Jinja2Templates

from .. import schemas
from .. import dependacy
from .utils import get_current_user
from db_client import errors as db_errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

orders_router = APIRouter(prefix="/orders", tags=["ORDERS"])
templates = Jinja2Templates(directory="./app/templates")

T = TypeVar("T")
P = ParamSpec("P")


# def _handle_db_errors(db_call: Callable[P, T]) -> Callable[P, T]:
#     @functools.wraps(db_call)
#     def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
#         try:
#             return db_call(*args, **kwargs)
#         except db_errors.UserNotFoundError:
#             return schemas.error.UserNotFoundResponse()
#         except db_errors.ChatNotFoundError:
#             return schemas.error.ChatNotFoundResponse()
#         except db_errors.ChatDoesNotBelongToUser:
#             return schemas.error.ChatDoesNotBelongToUserResponse()
#         except db_errors.DBError as exc:
#             return schemas.error.DBClientErrorResponse(message=str(exc))
#
#     return wrapper


@orders_router.get(
    "/create"
)
# @_handle_db_errors
def create_order(
    request: Request,
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):
    products = dependacy.customers_db_client.get_cart(customer_id=customer.customer_id)

    if not products:
        error_message = "No products in cart"
        return templates.TemplateResponse(
            "cart.html",
            {"request": request, "error": error_message}
        )

    order_id = dependacy.orders_db_client.add_order(
        date=datetime.datetime.now(),
        status="accepted",
        customer_id=customer.customer_id
    )

    for product in products:
        products_left = dependacy.products_db_client.get_product(product["product_id"])["quantity"]

        if products_left == 0:
            break

        dependacy.orders_db_client.add_product_to_order(
            product_id=product["product_id"],
            order_id=order_id,
            quantity=product["quantity"] if product["quantity"] < products_left else products_left,
            status="accepted"
        )

        dependacy.products_db_client.decrease_product_quantity(
            product_id=product["product_id"],
            quantity=product["quantity"]
        )

        dependacy.customers_db_client.delete_from_cart(
            customer_id=customer.customer_id, product_id=product["product_id"]
        )

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response

