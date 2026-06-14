from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/")
def get_menu_categories(request: Request):
    categories_list = ["Ropa", "Electrónica", "Hogar", "Accesorios"]
    return templates.TemplateResponse(
        request,
        "menu.html", 
        {"request": request, "categories": categories_list}
    )

@router.get("/items")
def get_menu_items(request: Request, category: str = None):
    return templates.TemplateResponse(
        request,
        "menu_items.html", 
        {"request": request, "category": category}
    )
