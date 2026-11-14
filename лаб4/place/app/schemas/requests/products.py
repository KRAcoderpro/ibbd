import datetime

from pydantic import BaseModel, StrictStr, Field, StrictInt


class AddProductBody(BaseModel):
    name: StrictStr = Field(..., min_length=2, max_length=255, description="Product name (2-255 symbols)")
    description: StrictStr = Field(..., min_length=11, max_length=255, description="Product description (11-255 symbols)")
    price: StrictInt = Field(..., description="Product price")
    discount: StrictInt | None = Field(..., description="Product discount")
    quantity: StrictInt = Field(..., description="Product quantity")
    store_id: StrictInt = Field(..., description="Product store id")


class AddProductReviewBody(BaseModel):
    grade: StrictInt = Field(..., description="Product review grade value")
    date: datetime.datetime = Field(..., description="Product review date")
    comment: StrictStr = Field(..., min_length=2, max_length=255, description="Product review comment")
    product_id: StrictInt = Field(..., description="Product id")
    customer_id: StrictInt = Field(..., description="Customer id")

