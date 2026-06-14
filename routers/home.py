from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Home"])

@router.get("/")
def get_home(request: Request):
    return templates.TemplateResponse(request, "home.html")