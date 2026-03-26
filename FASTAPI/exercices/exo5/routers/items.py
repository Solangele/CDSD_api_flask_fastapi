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


## Correction :
# from datetime import datetime
# from fastapi import APIRouter
# import db.memory as memory
# from models.response import ApiResponse, UserCreate, UserResponse

# router = APIRouter(tags=["Users Response"])


# @router.get("/users-response/{user_id}", response_model=ApiResponse[UserResponse])
# async def get_user_response(user_id: int):
#     if user_id not in memory.users_db:
#         return ApiResponse[UserResponse](
#             success=False,
#             data=None,
#             message=f"User with ID {user_id} not found"
#         )

#     user = memory.users_db[user_id]
#     user_response = UserResponse(**user)

#     return ApiResponse[UserResponse](
#         success=True,
#         data=user_response,
#         message="User retrieved successfully",
#         timestamp=datetime.now().isoformat()
#     )


# @router.post("/users-response", response_model=ApiResponse[None])
# async def create_user_response(user: UserCreate):
#     user_dict = user.model_dump()
#     user_dict["id"] = memory.next_user_id
#     memory.users_db[memory.next_user_id] = user_dict
#     memory.next_user_id += 1

#     return ApiResponse[None](
#         success=True,
#         data=None,
#         message="User created successfully",
#         timestamp=datetime.now().isoformat()
#     )