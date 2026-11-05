from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Date, Numeric,
    Boolean, Text, func
)
from sqlalchemy.orm import relationship
from database import Base


#Customer
class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
#Login
class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
#DeliveryPerson
class DeliveryPerson(Base):
    __tablename__ = "delivery_person"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
#Publication
class Publication(Base):
    __tablename__ = "publication"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    publication_type = Column(String(50), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Numeric, nullable=False)
    frequency = Column(Numeric, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
#Order
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    delivery_days=Column(String(100))
#Billing
class Billing(Base):
    __tablename__ = "billing"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    month = Column(String(100), nullable=False)
    total = Column(Numeric, nullable=False)


