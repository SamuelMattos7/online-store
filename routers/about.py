from fastapi import APIRouter, Request
from dependencies import templates

router = APIRouter(prefix="/about", tags=["About"])

@router.get("/")
def get_about(request: Request):
    return templates.TemplateResponse(request, "about.html")
