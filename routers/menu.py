from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import MenuItem
from db.database import get_db
from dependancies import templates
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/")
def get_menu_categories(request: Request):
    categories_list = ["Ropa", "Electrónica", "Hogar", "Accesorios"]
    return templates.TemplateResponse(
        request,
        "menu.html", 
        {"request": request, "categories": categories_list}
    )

@router.get("/menu-items")  
async def get_menu_items(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(MenuItem)
        .options(selectinload(MenuItem.category))
        .order_by(MenuItem.category_id)
    )
    items = result.scalars().all()
        
    grouped = {}
    for item in items:
        cat_name = item.category.name
        grouped.setdefault(cat_name, []).append(item)

    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={"grouped_items": grouped}
    )