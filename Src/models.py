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
#User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role= Column(String(50), nullable=False)
#DeliveryPerson
class DeliveryPerson(Base):
    __tablename__ = "delivery_person"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    area_id = Column(Integer, ForeignKey('delivery_area.id'), nullable=False)
#DeliveryArea
class DeliveryArea(Base):
    __tablename__ = "delivery_area"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
#Route
class Route(Base):
    __tablename__ = "route"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    driver_id=Column(Integer, ForeignKey('delivery_person.id'), nullable=False)
    status = Column(String(50), nullable=False)
#Publication
class Publication(Base):
    __tablename__ = "publication"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    publication_type = Column(String(50), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Numeric, nullable=False)
#Order
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    delivery_date=Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
#Order_Item
class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    publication_id = Column(Integer, ForeignKey('publication.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
#Billing
class Billing(Base):
    __tablename__ = "billing"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    amount=Column(Numeric(10,2), nullable=False)
    status = Column(String(50), nullable=False)
    due_date=Column(Date, nullable=False)

