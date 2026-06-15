from fastapi import APIRouter, Request
from dependencies import templates

router = APIRouter(tags=["Home"])

@router.get("/")
def get_home(request: Request):
    return templates.TemplateResponse(request, "home.html")