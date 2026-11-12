from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Date, Numeric,
    Boolean, Text, func
)
from sqlalchemy.orm import relationship
from database import Base


# Customer
class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(Text)

    # Relationships
    orders = relationship("Order", back_populates="customer")
    billings = relationship("Billing", back_populates="customer")

    def __repr__(self):
        return f"<Customer id={self.id} name={self.name} {self.last_name}>"


# User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"


# DeliveryArea
class DeliveryArea(Base):
    __tablename__ = "delivery_area"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationships
    delivery_persons = relationship("DeliveryPerson", back_populates="area")

    def __repr__(self):
        return f"<DeliveryArea id={self.id} name={self.name}>"


# DeliveryPerson
class DeliveryPerson(Base):
    __tablename__ = "delivery_person"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    area_id = Column(Integer, ForeignKey('delivery_area.id'), nullable=False)

    # Relationships
    area = relationship("DeliveryArea", back_populates="delivery_persons")
    routes = relationship("Route", back_populates="driver")

    def __repr__(self):
        return f"<DeliveryPerson id={self.id} name={self.name}>"


# Route
class Route(Base):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    driver_id = Column(Integer, ForeignKey('delivery_person.id'), nullable=False)
    status = Column(String(50), nullable=False)

    # Relationships
    driver = relationship("DeliveryPerson", back_populates="routes")

    def __repr__(self):
        return f"<Route id={self.id} date={self.date} status={self.status}>"


# Publication
class Publication(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    publication_type = Column(String(50), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order_items = relationship("OrderItem", back_populates="publication")

    def __repr__(self):
        return f"<Publication id={self.id} name={self.name} price={self.price}>"


# Order
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    delivery_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",   # deleting an order deletes its items
    )

    def __repr__(self):
        return (
            f"<Order id={self.id} customer_id={self.customer_id} "
            f"status={self.status} total={self.total_amount}>"
        )


# OrderItem
class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)  # ← fixed FK
    publication_id = Column(Integer, ForeignKey('publication.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    publication = relationship("Publication", back_populates="order_items")

    def __repr__(self):
        return (
            f"<OrderItem id={self.id} order_id={self.order_id} "
            f"publication_id={self.publication_id} qty={self.quantity}>"
        )


# Billing
class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False)
    due_date = Column(Date, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="billings")

    def __repr__(self):
        return (
            f"<Billing id={self.id} customer_id={self.customer_id} "
            f"amount={self.amount} status={self.status}>"
        )