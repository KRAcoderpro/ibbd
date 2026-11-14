from pydantic import BaseModel, StrictInt, StrictStr


class Customer(BaseModel):
    customer_id: StrictInt
    name: StrictStr
    phone: StrictStr


class Seller(BaseModel):
    seller_id: StrictInt
    inn: StrictStr
    name: StrictStr
    phone: StrictStr
    email: StrictStr
    address: StrictStr
    store_id: StrictInt
