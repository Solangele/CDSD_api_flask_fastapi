from fastapi import FastAPI
import uvicorn

from core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug
)

# app.include_router(users_router, prefix=settings.api_v1_prefix)
# app.include_router(auth_router, prefix=settings.api_v1_prefix)
# app.include_router(products_router, prefix=settings.api_v1_prefix)
# app.include_router(orders_router, prefix=settings.api_v1_prefix)
# app.include_router(users_response_router, prefix=settings.api_v1_prefix)
# app.include_router(info_router, prefix=settings.api_v1_prefix)
# app.include_router(events_router, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )