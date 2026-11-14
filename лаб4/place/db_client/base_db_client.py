from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import re


class BaseDBClient:
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)
        self._local_session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
        self._db: Session = self._local_session()

    def get_db(self) -> Session:
        return self._db

    @staticmethod
    def validate_phone(phone_number: str) -> str:
        validated = re.sub(r"[^\d]+", "", phone_number)

        validated = f"+{validated}" if not validated.startswith("+") else validated

        print(validated)

        return validated




