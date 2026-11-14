from pydantic import BaseModel, StrictStr, Field, StrictInt


class Customer(BaseModel):
    name: StrictStr = Field(..., min_length=2, max_length=255, description="Customer name (2-255 symbols)")
    customer_id: StrictInt = Field(..., description="Customer ID")

