from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import home, about, menu, cart, checkout
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Online Store",
    description="ecommerce restaurant for managing customers, menu items, and orders",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router)
app.include_router(about.router)
app.include_router(menu.router)
app.include_router(cart.router)
app.include_router(checkout.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
