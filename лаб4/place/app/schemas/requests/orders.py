import datetime

from pydantic import BaseModel, StrictStr, Field, StrictInt


class AddOrderBody(BaseModel):
    date: datetime.datetime = Field(..., description="Order review")
    status: StrictStr = Field(..., description="Order status")
    customer_id: StrictInt = Field(..., description="Customer id")


class AddProductToOrderBody(BaseModel):
    product_id: StrictInt = Field(..., description="Product id")
    order_id: StrictInt = Field(..., description="Order id")
    status: StrictStr = Field(..., description="Product status")
    quantity: StrictInt = Field(..., description="Product quantity")


class DeleteProductFromOrderBody(BaseModel):
    product_id: StrictInt = Field(..., description="Product id")
    order_id: StrictInt = Field(..., description="Order id")



