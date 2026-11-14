from pydantic import BaseModel, StrictInt, Field, StrictStr


class Seller(BaseModel):
    phone: StrictStr = Field(..., description="Seller id")
    store_id: StrictInt = Field(..., description="Store id")
