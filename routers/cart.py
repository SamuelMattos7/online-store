from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/")
def get_cart_items(request: Request):
    return templates.TemplateResponse(request, "cart.html", {"request": request, "cart": [], "total_items": 0, "subtotal": 0.0})

@router.post("/add")
def add_to_cart(request: Request, product_id: int, quantity: int = 1):
    return templates.TemplateResponse(
        request,
        "cart.html",
        {"request": request, "cart": [], "total_items": 0, "subtotal": 0.0}
    )

@router.delete("/remove/{product_id}")
def remove_from_cart(request: Request, product_id: int):
    return templates.TemplateResponse(
        request,
        "cart.html",
        {"request": request, "cart": [], "total_items": 0, "subtotal": 0.0}
    )
