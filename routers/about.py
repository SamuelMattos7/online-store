from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/about", tags=["About"])

@router.get("/")
def get_about(request: Request):
    return templates.TemplateResponse(request, "about.html")
