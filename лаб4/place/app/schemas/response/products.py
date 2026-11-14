import datetime

from pydantic import BaseModel, StrictStr, Field, StrictInt


class AllProductsResponse(BaseModel):
    class Product(BaseModel):
        product_id: StrictInt = Field(..., description="Product id")
        name: StrictStr = Field(..., min_length=2, max_length=255, description="Product name (2-255 symbols)")
        description: StrictStr = Field(..., min_length=11, max_length=255, description="Product description (11-255 symbols)")
        price: StrictInt = Field(..., description="Product price")
        discount: StrictInt | None = Field(..., description="Product discount")
        quantity: StrictInt = Field(..., description="Product quantity")
        store_id: StrictInt = Field(..., description="Product store id")

    products: list[Product]


