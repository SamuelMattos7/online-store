from __future__ import annotations
from datetime import UTC, datetime
from db.database import Base
from sqlalchemy import DateTime, ForeignKey, Table, Integer, String, Text, Boolean, Column, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

class StatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
class PaymentMethodEnum(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    
class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Costumer(Base):
    __tablename__ = 'costumers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

class DeliveryAddress(Base):
    __tablename__ = "delivery_address"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    costumer_id: Mapped[int] = mapped_column(
        ForeignKey("costumers.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False) 
    
class MenuCategory(Base):
    __tablename__ = 'menu_categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("menu_categories.id"),
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float(10), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    preparation_time: Mapped[int] = mapped_column(Integer(60), default=15, nullable=False)
    img_url: Mapped[str] = mapped_column(String(255), nullable=True)

class OrderStatus(Base):
    __tablename__ = "order_statuses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[StatusEnum] = mapped_column(String(50), default=StatusEnum.PENDING)
    
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    costumer_id: Mapped[int] = mapped_column(
        ForeignKey("costumer.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    delivery_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_address.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey("order_statuses.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    total_amount: Mapped[float] = mapped_column(Float(10), nullable=False)
    payment_method: Mapped[PaymentMethodEnum] = mapped_column(String(50), nullable=False)
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(String(50), default=PaymentStatusEnum.PENDING)
    delivery_fee: Mapped[float] = mapped_column(Float(10), default=0.0, nullable=False)
    estimated_delivery_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)     
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id"), 
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float(10), nullable=False)
    special_instructions: Mapped[str] = mapped_column(Text, nullable=True)
    
class OrderEvent(Base):
    __tablename__ = "order_events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), 
        nullable=False, 
        delete="CASCADE"
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_data: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
