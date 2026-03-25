from fastapi import APIRouter, HTTPException, status

from models.order import OrderCreate
from db import order_db

router = APIRouter(prefix= "/orders", tags = ["Orders"])

@router.post("/", response_model= dict, status_code= status.HTTP_201_CREATED)
async def create_order(order : OrderCreate) :
    order_dict = order.model_dump()
    order_dict["id"] = order_db.next_order_id
    order_db.orders_db[order_db.next_order_id] = order_dict
    order_db.next_order_id += 1

    return order_dict
