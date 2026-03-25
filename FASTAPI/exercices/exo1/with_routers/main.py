from fastapi import FastAPI
import uvicorn

from routers.users import router as users_router

app = FastAPI(title="Exercice FastAPI",version="1.0.0",description="Validation FASTAPI")

app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0',port=8000,reload=True)