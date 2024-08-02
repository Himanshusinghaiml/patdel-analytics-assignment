# # app/main.py
# from fastapi import FastAPI
# from routers import accounts, destinations, incoming_data
# from app.database import engine, Base

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(accounts.router)
# app.include_router(destinations.router)
# app.include_router(incoming_data.router)
# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#---------------------------------------------------------#
# this routes define to create accounts
@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)
#this routes define to access the account user 
@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
#-----------------------------------------------------------#


#-----------------------------------------------------------#
# this routes define to create destination  with each unique accounts 
@app.post("/accounts/{account_id}/destinations/", response_model=schemas.Destination)
def create_destination_for_account(
    account_id: int, destination: schemas.DestinationCreate, db: Session = Depends(get_db)
):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return crud.create_destination(db=db, destination=destination, account_id=account_id)


# this routes define to accesss all the destinations 
@app.get("/accounts/{account_id}/destinations/", response_model=List[schemas.Destination])
def get_destinations(account_id: int, db: Session = Depends(get_db)):
    db_destinations = crud.get_destinations(db, account_id)
    if db_destinations is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_destinations

#---------------------------------------------------------------#

@app.post("/server/incoming_data/")
def receive_data(data: dict, x_token: str ='eb989357bb8de4d71ee488173711a7c3', db: Session = Depends(get_db)):
    print(f"Received token: {x_token}")
    db_account = db.query(models.Account).filter(models.Account.app_secret_token == x_token).first()
    if not db_account:
        raise HTTPException(status_code=401, detail="Unauthenticated")

    for destination in db_account.destinations:
        send_data_to_destination(destination, data)

    return {"status": "data sent"}

def send_data_to_destination(destination, data):
    import requests
    headers = destination.headers
    url = destination.url
    method = destination.http_method.upper()
    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response.status_code
