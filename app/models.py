# # app/models.py
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from .database import Base

# class Account(Base):
#     __tablename__ = "accounts"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     account_name = Column(String, nullable=False)
#     app_secret_token = Column(String, unique=True, nullable=False)
#     website = Column(String, nullable=True)
#     destinations = relationship("Destination", back_populates="account", cascade="all, delete-orphan")

# class Destination(Base):
#     __tablename__ = "destinations"
    
#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, nullable=False)
#     http_method = Column(String, nullable=False)
#     headers = Column(String, nullable=False)
#     account_id = Column(Integer, ForeignKey("accounts.id"))
#     account = relationship("Account", back_populates="destinations")

from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    account_name = Column(String, index=True)
    app_secret_token = Column(String, index=True)
    website = Column(String, index=True, nullable=True)
    destinations = relationship("Destination", back_populates="account")

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    http_method = Column(String, index=True)
    headers = Column(JSON)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="destinations")
