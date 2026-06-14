from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- ADDRESS SCHEMAS ---
class AddressCreate(BaseModel):
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    instructions: Optional[str] = None
    is_default: bool = False

class AddressResponse(AddressCreate):
    id: int
    customer_id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- CUSTOMER SCHEMAS ---
class CustomerCreate(BaseModel):
    email: EmailStr
    phone: str = Field(..., max_length=20)
    full_name: str = Field(..., max_length=255)

class CustomerResponse(CustomerCreate):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- CATEGORY SCHEMAS ---
class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    sort_order: int = 0

class CategoryResponse(CategoryCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- MENU ITEM SCHEMAS ---
class MenuItemCreate(BaseModel):
    category_id: int
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    is_available: bool = True
    preparation_time_minutes: int = Field(15, ge=1)
    image_url: Optional[str] = None

class MenuItemResponse(MenuItemCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# --- ORDER ITEMS ---
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    special_instructions: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal  # Captured snapshot of price at order time
    special_instructions: Optional[str]

    model_config = ConfigDict(from_attributes=True)

# --- ORDERS ---
class OrderCreate(BaseModel):
    address_id: int
    payment_method: str = Field(..., max_length=50)  # card, cash, online
    # Client sends an array of menu items they want to buy
    items: List[OrderItemCreate] = Field(..., min_length=1)

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    address_id: int
    order_status_id: int
    placed_at: datetime
    updated_at: datetime
    total_amount: Decimal
    payment_method: str
    payment_status: str
    delivery_fee: Decimal
    estimated_delivery_time: Optional[datetime]
    
    # We can automatically nest the item rows inside the response
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

# --- ORDER TIMELINE EVENTS ---
class OrderEventResponse(BaseModel):
    id: int
    order_id: int
    event_type: str
    event_data: Optional[dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Minimal Customer Data
class CustomerNested(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    
    model_config = ConfigDict(from_attributes=True)

# Minimal Address Data
class AddressNested(BaseModel):
    id: int
    street: str
    city: str
    zip_code: Optional[str]
    instructions: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

# Minimal Menu Item Data (so the client knows what they ordered)
class MenuItemNested(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

class OrderItemDetailedResponse(BaseModel):
    id: int
    quantity: int
    unit_price: Decimal          # Price frozen at the moment of purchase
    special_instructions: Optional[str]
    menu_item: MenuItemNested    # Joins the menu item data
    
    model_config = ConfigDict(from_attributes=True)

class OrderDetailsResponse(BaseModel):
    id: int
    placed_at: datetime
    updated_at: datetime
    total_amount: Decimal
    delivery_fee: Decimal
    payment_method: str
    payment_status: str
    estimated_delivery_time: Optional[datetime]
    
    # 1. Joins the current textual string of the status lookup table
    status: str 
    
    # 2. Rich nested database relationships
    customer: CustomerNested
    delivery_address: AddressNested
    items: List[OrderItemDetailedResponse]

    model_config = ConfigDict(from_attributes=True)

