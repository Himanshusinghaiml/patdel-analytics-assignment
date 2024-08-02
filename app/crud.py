
from sqlalchemy.orm import Session
from . import models, schemas

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(email=account.email, account_name=account.account_name, website=account.website)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def create_destination(db: Session, destination: schemas.DestinationCreate, account_id: int):
    db_destination = models.Destination(url=str(destination.url), http_method=destination.http_method, headers=destination.headers, account_id=account_id)
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

def get_destinations(db: Session, account_id: int):
    return db.query(models.Destination).filter(models.Destination.account_id == account_id).all()

