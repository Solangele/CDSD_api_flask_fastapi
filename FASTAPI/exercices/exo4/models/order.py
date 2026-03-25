from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from typing import Optional
import uuid


class Items(BaseModel):
    product_id : int = Field(..., description= "item id")
    quantity : int = Field(...,ge = 1, description= "item quantity")
    price : float = Field(..., gt = 0,  description= "item price")



class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id : uuid.UUID = Field(..., description= "Order ID")
    customer_email : EmailStr = Field(..., description= "valid email")
    items : list[Items] = Field(..., min_length= 1, description= "order list")
    total : float = Field(0, description= "Total order")


    @model_validator(mode= "after")
    def calculate_total(self) -> 'OrderCreate' :
        total_calcul = sum(item.price * item.quantity for item in self.items)
        self.total = total_calcul
        return self