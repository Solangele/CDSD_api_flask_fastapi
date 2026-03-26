from fastapi import FastAPI
import uvicorn

from routers.orders import router as products_router

app = FastAPI(title="Exercice4 FastAPI",version="1.0.0",description="Validation FASTAPI")

app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0',port=8000,reload=True)
    