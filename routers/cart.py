from fastapi import APIRouter, Request, Depends
from dependencies import templates
from models.models import MenuItem
from db.database import get_db
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/")
async def get_cart_items(request: Request,  db: AsyncSession = Depends(get_db)):
    session_cart = request.session.get("cart", {})
    
    cart_items = []
    subtotal = 0.0
    
    if session_cart:
        product_ids = [int(pid) for pid in session_cart.keys()]
        
        result = await db.execute(select(MenuItem).where(MenuItem.id.in_(product_ids)))
        products = result.scalars().all()
        
        for product in products:
            quantity = session_cart[str(product.id)]
            item_total = product.price * quantity
            subtotal += item_total
            
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total
            })
            
    return templates.TemplateResponse(
        request=request,               
        name="cart.html",              
        context={
            "cart_items": cart_items, 
            "subtotal": subtotal
        }
    )

@router.post("/add")
def add_to_cart(request: Request, product_id: int, quantity: int = 1):
    cart = request.session.get("cart", {})
    
    str_id = str(product_id)
    if str_id in cart:
        cart[str_id] += quantity
    else:
        cart[str_id] = quantity

    request.session["cart"] = cart
    
    return {
        "status": "success",
        "total_items": sum(cart.values()),
        "new_quantity": cart[str_id] 
    }

@router.delete("/remove/{product_id}")
async def remove_from_cart(request: Request, product_id: int):
    cart = request.session.get("cart", {})
    str_id = str(product_id)
    if str_id in cart:
        del cart[str_id]
        request.session["cart"] = cart
    # total_items = sum(cart.values())
    return {
        "status": "success",
        "message": f"Producto {product_id} eliminado del carrito"
    }

@router.post("/decrease")
def decrease_cart_item(request: Request, product_id: int):
    cart = request.session.get("cart", {})
    str_id = str(product_id)
    
    new_quantity = 0
    if str_id in cart:
        cart[str_id] -= 1
        new_quantity = cart[str_id]
        
        if cart[str_id] <= 0:
            del cart[str_id]
            new_quantity = 0

    request.session["cart"] = cart
    return {
        "status": "success",
        "total_items": sum(cart.values()),
        "new_quantity": new_quantity
    }
