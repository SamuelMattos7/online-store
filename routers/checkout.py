from fastapi import APIRouter, HTTPException, Request
from dependencies import templates

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/summary")
def get_checkout_summary(request: Request):
    return templates.TemplateResponse(
        request,
        "checkout_summary.html",
        {"request": request, "shipping_cost": 5.0, "tax": 1.2, "final_total": 6.2}
    )

@router.post("/place-order")
def place_order(request: Request, payment_method: str):
    if payment_method not in ["card", "paypal"]:
        raise HTTPException(status_code=400, detail="Método de pago no soportado")
    return templates.TemplateResponse(
        request,
        "order_confirmation.html",
        {"request": request, "status": "success", "order_id": 9999, "message": "Pedido realizado con éxito"}
    )
