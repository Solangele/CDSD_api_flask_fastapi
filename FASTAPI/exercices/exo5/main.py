from fastapi import FastAPI
from models.schema import ApiResponse
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

@app.get("/user", response_model=ApiResponse[User])
async def get_user():
    user_data = User(username="Alice", email="alice@example.com")
    return ApiResponse(data=user_data, message="Utilisateur trouvé")

@app.get("/ping", response_model=ApiResponse[str])
async def ping():
    return ApiResponse(data="pong", message="Le serveur répond bien")