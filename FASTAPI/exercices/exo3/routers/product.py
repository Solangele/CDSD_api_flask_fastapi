from fastapi import APIRouter
from pydantic import BaseModel, field_validator, Field, ConfigDict, model_validator, EmailStr
from typing import Optional
from enum import Enum
import re


router = APIRouter(
    prefix= "/products",
    tags= ["Gestion des produits"]
)

class TypeCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    OTHER = "other"


class Supplier(BaseModel):
    name : str = Field(..., description= "supplier name")
    email : EmailStr = Field(..., description= "supplier email")
    phone : Optional[str] = Field(None, description= "supplier phone number")



class Products(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name : str = Field(..., description= "Product name")
    price : float = Field(..., gt = 0)
    category : TypeCategory = Field(..., description= "Product category")
    stock : int = Field(..., ge = 0)
    supplier : Supplier


@router.post("/product", response_model=Products)
async def create_product(product: Products):
    return product