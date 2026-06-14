from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from models.models import PaymentMethodEnum, PaymentStatusEnum, StatusEnum

# --- ADDRESS SCHEMAS ---
class AddressCreate(BaseModel):
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    instructions: Optional[str] = None
    is_default: bool = False

class AddressResponse(AddressCreate):
    id: int
    costumer_id: int                                        
    
    model_config = ConfigDict(from_attributes=True)

class AddressNested(BaseModel):
    id: int
    street: str
    city: str
    zip_code: Optional[str]
    instructions: Optional[str]
    
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

class CustomerNested(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    
    model_config = ConfigDict(from_attributes=True)


# --- CATEGORY SCHEMAS ---
class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    sort_order: int = 0

class CategoryResponse(CategoryCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class CategoryNested(BaseModel):                            
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)


# --- MENU ITEM SCHEMAS ---
class MenuItemCreate(BaseModel):
    category_id: int
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    is_available: bool = True
    preparation_time: int = Field(15, ge=1)                 
    img_url: Optional[str] = None                           

class MenuItemResponse(BaseModel):                          
    id: int                                                 
    category: CategoryNested                                
    name: str
    description: Optional[str]
    price: Decimal
    is_available: bool
    preparation_time: int                                   
    img_url: Optional[str]                                  
    
    model_config = ConfigDict(from_attributes=True)

class MenuItemNested(BaseModel):
    id: int
    name: str
    img_url: Optional[str]                                  
    
    model_config = ConfigDict(from_attributes=True)


# --- ORDER ITEM SCHEMAS ---
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    special_instructions: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    special_instructions: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class OrderItemDetailedResponse(BaseModel):
    id: int
    quantity: int
    unit_price: Decimal
    special_instructions: Optional[str]
    menu_item: MenuItemNested

    model_config = ConfigDict(from_attributes=True)


# --- ORDER SCHEMAS ---
class OrderCreate(BaseModel):
    delivery_id: int                                        
    payment_method: PaymentMethodEnum                       
    items: List[OrderItemCreate] = Field(..., min_length=1)

class OrderResponse(BaseModel):
    id: int
    costumer_id: int                                        
    delivery_id: int                                        
    status: StatusEnum                                      
    placed_at: datetime
    updated_at: datetime
    total_amount: Decimal
    payment_method: PaymentMethodEnum                       
    payment_status: PaymentStatusEnum                       
    delivery_fee: Decimal
    estimated_delivery_time: Optional[datetime]
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

class OrderDetailsResponse(BaseModel):
    id: int
    placed_at: datetime
    updated_at: datetime
    total_amount: Decimal
    delivery_fee: Decimal
    payment_method: PaymentMethodEnum                       
    payment_status: PaymentStatusEnum                       
    estimated_delivery_time: Optional[datetime]
    status: StatusEnum                                      
    customer: CustomerNested
    delivery_address: AddressNested
    items: List[OrderItemDetailedResponse]
    events: List["OrderEventResponse"] = []                 

    model_config = ConfigDict(from_attributes=True)


# --- ORDER EVENT SCHEMAS ---
class OrderEventCreate(BaseModel):                          
    order_id: int
    event_type: str
    event_data: Optional[dict[str, Any]] = None

class OrderEventResponse(BaseModel):
    id: int
    order_id: int
    event_type: str
    event_data: Optional[dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


OrderDetailsResponse.model_rebuild()

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., max_length=255)
    costumer_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    costumer: Optional[CustomerNested] = None               
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel): 
    name: Optional[str] = None
    email: Optional[EmailStr] = None
