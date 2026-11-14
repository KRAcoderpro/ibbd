from fastapi import Depends, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from .utils import get_current_user
from .. import schemas
from .. import dependacy
from .utils import get_current_user

templates = Jinja2Templates(directory="./app/templates")

view_router = APIRouter(tags=["VIEW"])


@view_router.get("/", response_class=HTMLResponse, name="main_page")
def index(
        request: Request,
        user: schemas.response.custoemrs.Customer = Depends(get_current_user)

):
    products = dependacy.products_db_client.get_all_products()

    return templates.TemplateResponse(
        "index.html", {"request": request, "products": products}
    )

