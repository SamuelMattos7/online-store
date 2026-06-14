from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from connection import MenuItem

from db.database import get_db
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

@router.get("/menu-items")  
async def get_menu_items(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(MenuItem))
    items = result.scalars().all()
    
    return templates.TemplateResponse(
        "menu_items.html",
        {"request": request, "items": items}
    )