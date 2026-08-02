from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Store Admin API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products_router)
app.include_router(orders_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/database")
def database_health_chekc() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "ok"}
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from error
