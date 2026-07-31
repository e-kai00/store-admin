from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine


app = FastAPI(title="Store Admin API")

@app.get("/health")
def health_check() -> dict[str, str]:
	return {"status": "ok"}

@app.get("/health/database")
def database_health_chekc() -> dict[str, str]:
	try: 
		with engine.connect() as connection:
			connection.execute(text("SELECT 1"))
		return {"database": "ok"}
	except SQLAlchemyError  as error:
		raise HTTPException(
			status_code=503,
			detail="Database unavailable",
		) from error
