from .common import DBError


class SellerAlreadyExistsError(DBError):
    pass


class SellerNotFoundError(DBError):
    pass


class StoreWithSellerExistsError(DBError):
    pass


class StoreWithNameExistsError(DBError):
    pass
