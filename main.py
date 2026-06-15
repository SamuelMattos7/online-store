from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers import home, about, menu, cart, checkout
from fastapi.staticfiles import StaticFiles
from dependencies import templates, load
import os  

app = FastAPI(
    title="Online Store",
    description="ecommerce restaurant for managing customers, menu items, and orders",
    version="1.0.0"
)

SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    session_cookie="session",       
    max_age=14 * 24 * 60 * 60,      
    same_site="lax",               
    https_only=False                
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_cart_total_items(request):
    if not request:
        return 0
    cart = request.session.get("cart", {})
    return sum(cart.values())

templates.env.globals["get_cart_total_items"] = get_cart_total_items

app.include_router(home.router)
app.include_router(about.router)
app.include_router(menu.router)
app.include_router(cart.router)
app.include_router(checkout.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
