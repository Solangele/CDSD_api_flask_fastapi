# ## Exercice 3: Modèles Imbriqués

# **Énoncé**:
# Créez une structure pour un `Produit` contenant:
# - `name`: nom du produit
# - `price`: prix (> 0)
# - `category`: catégorie (énumération: ELECTRONICS, CLOTHING, FOOD, OTHER)
# - `stock`: entier (>= 0)
# - `supplier`: objet Pydantic avec:
#   - `name`: nom du fournisseur
#   - `email`: email du fournisseur
#   - `phone`: téléphone (optionnel)


from fastapi import FastAPI
from pydantic import BaseModel, field_validator, Field, ConfigDict, model_validator, EmailStr
from typing import Optional
from enum import Enum
import re


app = FastAPI(
    title="FastAPI exo3",
    description="password validation",
    version="1.0.0"
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


@app.post("/product", response_model=Products)
async def create_user(product: Products):
    return product
