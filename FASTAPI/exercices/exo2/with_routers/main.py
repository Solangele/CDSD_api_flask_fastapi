from fastapi import FastAPI
import uvicorn

from routers.authentification import router as auth_router

app = FastAPI(title="Exercice FastAPI",version="1.0.0",description="Validation FASTAPI")

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0',port=8000,reload=True)