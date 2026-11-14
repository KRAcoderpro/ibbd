from .common import DBError


class CustomerAlreadyExistsError(DBError):
    pass


class CustomerNotFoundError(DBError):
    pass


class NoProductInCart(DBError):
    pass


class NoProductsLeft(DBError):
    pass


class StoreWithSellerExistsError(DBError):
    pass


class StoreWithNameExistsError(DBError):
    pass
