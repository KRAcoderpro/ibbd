import functools
from datetime import timedelta

from fastapi import Depends, APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import logging
from typing import TypeVar, ParamSpec
from db_client.errors import seller_errors as seller_db_errors
from .. import schemas
from .. import dependacy
from .utils import get_current_seller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

seller_router = APIRouter(prefix="/sellers", tags=["SELLERS"])
templates = Jinja2Templates(directory="./app/templates")

T = TypeVar("T")
P = ParamSpec("P")


@seller_router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register_seller.html", {"request": request, "error": None})


@seller_router.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login_seller.html", {"request": request, "error": None})


@seller_router.get("/account", response_class=HTMLResponse)
async def show_account(
        request: Request,
        seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):
    store_catalog = dependacy.products_db_client.get_store_products(
        store_id=seller.store_id
    )

    seller_all_orders = dependacy.orders_db_client.get_store_orders(
        store_id=seller.store_id
    )
    return templates.TemplateResponse(
        "seller_account.html", {
            "request": request,
            "error": None,
            "store_catalog": store_catalog,
            "seller_all_orders": seller_all_orders
        }
    )


@seller_router.post("/register", response_class=HTMLResponse)
def register_seller(
        request: Request,
        inn=Form(...),
        phone=Form(...),
        email=Form(...),
        address=Form(...),
        name=Form(...),
        store_name=Form(...),
        store_description=Form(...),
):
    try:
        seller_id = dependacy.seller_db_client.add_seller(
            inn=inn,
            phone=phone,
            email=email,
            address=address,
            name=name
        )
    except seller_db_errors.SellerAlreadyExistsError():
        error_message = f"Seller with provided data is already taken."
        return templates.TemplateResponse(
            "register_seller.html",
            {"request": request, "error": error_message, "name": name, "phone": phone}
        )

    store_id = dependacy.seller_db_client.add_store(
        seller_id=seller_id,
        store_name=store_name,
        store_description=store_description
    )

    access_token = dependacy.jwt_encryption.create_access_token(
        {
            "phone": phone,
            "store_id": store_id
        }
    )

    response = RedirectResponse(url="/sellers/account", status_code=303)
    response.set_cookie(
        key="seller_token",
        value=access_token,
        httponly=True,
        max_age=1800  # Время жизни куки в секундах (30 минут)
    )
    return response


@seller_router.post("/login", response_class=HTMLResponse)
# @_handle_db_errors
def login_seller(
        request: Request,
        phone=Form(...)
):
    seller = dependacy.seller_db_client.get_seller_by_phone(
        phone=phone
    )

    if seller is None:
        error_message = f"Seller with provided phone '{phone}' not found."
        return templates.TemplateResponse(
            "login_seller.html",
            {"request": request, "error": error_message, "phone": phone}
        )

    access_token = dependacy.jwt_encryption.create_access_token(
        {
            "phone": seller.phone,
            "store_id": seller.store_id
        }
    )

    response = RedirectResponse(url="/sellers/account", status_code=303)
    response.set_cookie(
        key="seller_token",
        value=access_token,
        httponly=True,
        max_age=1800  # Время жизни куки в секундах (30 минут)
    )
    return response


@seller_router.post(
    "/add/store"
)
def add_store(
        add_store_body: schemas.requests.seller.AddStoreBody,
):

    dependacy.seller_db_client.add_store(
        store_name=add_store_body.name,
        store_description=add_store_body.description,
        seller_id=add_store_body.seller_id
    )


@seller_router.get("/logout")
async def logout_user():
    response = RedirectResponse(url="/sellers/login")
    response.delete_cookie(key="seller_token")
    return response


@seller_router.delete(
    "/delete"
)
def delete_seller(
        seller_id: int
):

    dependacy.seller_db_client.delete_seller_by_id(seller_id=seller_id)

    return RedirectResponse(url="/sellers/logout", status_code=303)

