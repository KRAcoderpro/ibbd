from sqlalchemy.orm import Session

from . import models, structures
from .errors import seller_errors, DBError
from .base_db_client import BaseDBClient


class SellerDBClient:
    def __init__(self, db_client: BaseDBClient):
        self._db_client = db_client
        self._db: Session = self._db_client.get_db()

    def add_seller(
            self, inn: str, name: str, email: str, phone: str, address: str
    ) -> int:
        phone = self._db_client.validate_phone(phone)

        db_seller = self._db.query(models.Seller).filter(
            models.Seller.inn == inn).first()
        if db_seller:
            raise seller_errors.SellerAlreadyExistsError()

        new_seller = models.Seller(
            inn=inn,
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        try:
            self._db.add(new_seller)
            self._db.commit()
            self._db.refresh(new_seller)
            return new_seller.seller_id
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def get_seller_by_phone(
            self, phone: str
    ) -> structures.Seller | None:
        phone = self._db_client.validate_phone(phone)

        db_seller = self._db.query(models.Seller).filter(
            models.Seller.phone == phone).first()

        if db_seller is None:
            return None

        seller: dict = db_seller.__dict__
        seller.update({"store_id": db_seller.store[0].store_id})
        return structures.Seller(**seller)

    def add_store(self, seller_id: int, store_name: str,
                  store_description: str) -> int:
        # db_seller = self._db.query(models.Seller).filter(
        #     models.Seller.seller_id == seller_id
        # ).first()
        # if not db_seller:
        #     raise seller_errors.SellerNotFoundError()
        #
        # if db_seller:
        #     raise seller_errors.StoreWithSellerExistsError()
        #
        # db_seller = self._db.query(models.Seller).filter(
        #     models.Seller.name == store_name
        # ).first()
        #
        # if db_seller:
        #     raise seller_errors.StoreWithNameExistsError()

        new_store = models.Store(
            seller_id=seller_id,
            name=store_name,
            description=store_description
        )
        try:
            self._db.add(new_store)
            self._db.commit()
            self._db.refresh(new_store)
            return new_store.store_id
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc

    def delete_seller_by_id(self, seller_id: int) -> None:
        seller = self._db.query(models.Seller).filter(
            models.Seller.seller_id == seller_id).first()
        if seller is None:
            raise seller_errors.SellerNotFoundError()

        try:
            self._db.delete(seller)
            self._db.commit()
        except Exception as exc:
            self._db.rollback()
            raise DBError() from exc
