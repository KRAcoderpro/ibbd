from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_client import models
db_url = "postgresql://root:Passw0rd12@localhost:5432/marketplace"

engine = create_engine(db_url)
local_session = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
db = local_session()

try:
    customer = db.query(models.Customer).filter(
        models.Customer.phone == "+79006440042"
    ).first()

    db.delete(customer)
    db.commit()
except Exception as exc:
    db.rollback()
    print(str(exc))





