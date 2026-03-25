from fastapi import FastAPI
from routers.product import router as product_router

app = FastAPI(
    title = "FastAPI exo3 with routers",
    version= "1.0.0"
)

app.include_router(product_router)

@app.get("/")
async def welcome():
    return {"message" : "Bienvenue sur l'API de l'exercice 3"}