from pydantic import BaseModel, EmailStr, StrictStr, Field, StrictInt


class RegisterSellerBody(BaseModel):
    inn: StrictStr = Field(..., min_length=10, max_length=12, description="Seller inn (10-12 symbols)")
    name: StrictStr = Field(..., min_length=2, max_length=255, description="Seller name (2-255 symbols)")
    phone: StrictStr = Field(..., min_length=11, max_length=20, description="Seller phone (11-20 symbols)")
    email: EmailStr
    address: StrictStr = Field(..., min_length=10, max_length=255, description="Seller address (10-255 symbols)")


class AddStoreBody(BaseModel):
    name: StrictStr = Field(..., min_length=2, max_length=50, description="Seller name (2-50 symbols)")
    description: StrictStr = Field(..., min_length=10, max_length=255, description="Seller name (10-255 symbols)")
    seller_id: StrictInt

