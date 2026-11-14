from pydantic import BaseModel, StrictStr, Field


class RegisterCustomerBody(BaseModel):
    name: StrictStr = Field(..., min_length=2, max_length=255, description="Customer name (2-255 symbols)")
    phone: StrictStr = Field(..., min_length=11, max_length=20, description="Customer phone (11-20 symbols)")

