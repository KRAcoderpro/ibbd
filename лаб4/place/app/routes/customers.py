from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
import logging
from typing import TypeVar, ParamSpec
from db_client.errors import customer_errors as customer_db_errors
from .utils import get_current_user
from .. import dependacy
from fastapi.templating import Jinja2Templates
from .. import schemas
# from .utils import get_current_user
from db_client import errors as db_errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="./app/templates")

customers_router = APIRouter(prefix="/customers", tags=["CUSTOMERS"])

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

@customers_router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@customers_router.get("/login", response_class=HTMLResponse)
async def login_register_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@customers_router.get("/logout")
async def logout_user():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response


@customers_router.get("/cart", response_class=HTMLResponse)
async def get_cart(
    request: Request,
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):
    products = dependacy.customers_db_client.get_cart(customer.customer_id)
    return templates.TemplateResponse(
        "cart.html",
        {"request": request, "error": None, "products": products}
    )


@customers_router.get("/account", response_class=HTMLResponse)
async def get_account(
    request: Request,
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):

    orders = dependacy.orders_db_client.get_orders(customer.customer_id)

    return templates.TemplateResponse(
        "account.html",
        {"request": request, "error": None, "orders": orders, "customer": customer}
    )


@customers_router.post("/register", response_class=HTMLResponse)
# @_handle_db_errors
def register_customer(
    request: Request,
    name=Form(...),
    phone=Form(...)
):
    try:
        customer_id = dependacy.customers_db_client.add_customer(
            name=name,
            phone=phone
        )
    except customer_db_errors.CustomerAlreadyExistsError():
        error_message = f"User with provided phone '{phone}' is already taken."
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": error_message, "name": name, "phone": phone}
        )

    access_token = dependacy.jwt_encryption.create_access_token(
        {
            "customer_id": customer_id,
            "name": name
        }
    )

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800  # Время жизни куки в секундах (30 минут)
    )
    return response


@customers_router.post("/login", response_class=HTMLResponse)
# @_handle_db_errors
def login_customer(
    request: Request,
    phone=Form(...)
):
    customer = dependacy.customers_db_client.get_customer_by_phone(
        phone=phone
    )

    if customer is None:
        error_message = f"User with provided phone '{phone}' not found."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error_message, "phone": phone}
        )

    access_token = dependacy.jwt_encryption.create_access_token(
        {
            "customer_id": customer.customer_id,
            "name": customer.name
        }
    )

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800  # Время жизни куки в секундах (30 минут)
    )
    return response


@customers_router.get(
    "/delete",
    response_class=HTMLResponse
)
# @_handle_db_errors
def delete_customer(
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):

    dependacy.customers_db_client.delete_customer(
        customer_id=customer.customer_id
    )

    return RedirectResponse(url="/customers/logout", status_code=303)


@customers_router.get("/cart/add/{product_id}", response_class=HTMLResponse)
# @_handle_db_errors
def add_product_to_cart(
    request: Request,
    product_id: int,
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):
    dependacy.customers_db_client.add_to_cart(
        customer_id=customer.customer_id,
        product_id=product_id,
        quantity=1
    )

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response


@customers_router.get("/cart/remove/{product_id}", response_class=HTMLResponse)
# @_handle_db_errors
def remove_product_from_cart(
    request: Request,
    product_id: int,
    customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):

    dependacy.customers_db_client.remove_from_cart(
        customer_id=customer.customer_id,
        product_id=product_id,
    )

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response


@customers_router.get("/cart/delete/{product_id}", response_class=HTMLResponse)
# @_handle_db_errors
def delete_product_from_cart(
        request: Request,
        product_id: int,
        customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):
    dependacy.customers_db_client.delete_from_cart(
        customer_id=customer.customer_id,
        product_id=product_id,
    )

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response
