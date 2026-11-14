import datetime
import functools

from fastapi import Depends, APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
import logging
from typing import TypeVar, ParamSpec, Callable
from fastapi.templating import Jinja2Templates
from .utils import get_current_user, get_current_seller

from .. import schemas
from .. import dependacy
from db_client import errors as db_errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

products_router = APIRouter(prefix="/products", tags=["PRODUCTS"])
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


@products_router.get("/add", response_class=HTMLResponse)
async def show_add_product(
        request: Request,
        seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):
    return templates.TemplateResponse("add_product.html", {"request": request, "error": None})


@products_router.get("/edit/{product_id}", response_class=HTMLResponse)
async def show_edit_product(
        request: Request,
        product_id: int,
        seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):
    product = dependacy.products_db_client.get_product(product_id)
    return templates.TemplateResponse(
        "edit_product.html",
        {
            "request": request,
            "error": None,
            "product": product
        }
    )


@products_router.get(
    "/{product_id}"
)
# @_handle_db_errors
def get_product(
        request: Request,
        product_id: int,
        customer: schemas.response.custoemrs.Customer = Depends(get_current_user)
):

    product = dependacy.products_db_client.get_product(product_id)
    reviews = dependacy.products_db_client.get_product_reviews(product_id)

    is_review = False
    for review in reviews:
        db_customer = dependacy.customers_db_client.get_customer(customer.customer_id)
        if review["customer_id"] == db_customer.customer_id:
            is_review = True
            break

    return templates.TemplateResponse(
        "product.html",
        {"request": request, "error": None, "product": product, "reviews": reviews, "is_review": is_review}
    )


@products_router.post(
    "/add",
    response_class=HTMLResponse
)
# @_handle_db_errors
def add_product(
    name=Form(...),
    description=Form(...),
    price=Form(...),
    discount=Form(...),
    quantity=Form(...),
    seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):

    dependacy.products_db_client.add_product(
        name=name,
        description=description,
        price=price,
        discount=discount,
        quantity=quantity,
        store_id=seller.store_id
    )

    return RedirectResponse(url="/sellers/account", status_code=303)


@products_router.post(
    "/edit/{product_id}",
    response_class=HTMLResponse
)
# @_handle_db_errors
def edit_product(
    product_id: int,
    name=Form(...),
    description=Form(...),
    price=Form(...),
    discount=Form(...),
    quantity=Form(...),
    seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):
    product = dependacy.products_db_client.get_product(product_id)

    if product["store_id"] != seller.store_id:
        return RedirectResponse(url="/sellers/logout", status_code=303)

    dependacy.products_db_client.update_product(
        product_id=product_id,
        name=name,
        description=description,
        price=price,
        discount=discount,
        quantity=quantity,
    )

    return RedirectResponse(url="/sellers/account", status_code=303)


@products_router.post(
    "/add/review/{product_id}"
)
# @_handle_db_errors
def add_product_review(
        request: Request,
        product_id: int,
        comment: str = Form(...),
        grade: int = Form(...),
        customer: schemas.response.custoemrs.Customer = Depends(get_current_user)

):

    dependacy.products_db_client.add_product_review(
        grade=grade,
        date=datetime.datetime.now(),
        comment=comment,
        product_id=product_id,
        customer_id=customer.customer_id
    )

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response


@products_router.get(
    "/get/all"
)
# @_handle_db_errors
def get_all_products():

    products = dependacy.products_db_client.get_all_products()

    return schemas.response.products.AllProductsResponse(**{"products": products})


@products_router.get(
    "/delete/{product_id}",
    response_class=HTMLResponse

)
# @_handle_db_errors
def delete_product(
    request: Request,
    product_id: int,
    seller: schemas.response.sellers.Seller = Depends(get_current_seller)
):
    product = dependacy.products_db_client.get_product(product_id)

    if product["store_id"] != seller.store_id:
        return RedirectResponse(url="/sellers/logout", status_code=303)

    dependacy.products_db_client.delete_product_by_id(product_id=product_id)

    referer = request.headers.get("referer")

    if referer:
        response = RedirectResponse(url=referer, status_code=303)
    else:
        response = RedirectResponse(url="/", status_code=303)

    return response

