from fastapi import APIRouter
from models.schema import ApiResponse
from pydantic import BaseModel

router = APIRouter(prefix="/test", tags=["Génériques"])

class Product(BaseModel):
    name: str
    price: float

@router.get("/product", response_model=ApiResponse[Product])
async def get_single_product():
    my_product = Product(name="Clavier RGB", price=49.99)
    
    return ApiResponse(
        data=my_product,
        message="Produit récupéré avec succès"
    )

@router.get("/info", response_model=ApiResponse[str])
async def get_status():
    return ApiResponse(
        data="Serveur Opérationnel",
        message="Status check"
    )