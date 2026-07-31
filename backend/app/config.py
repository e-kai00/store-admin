from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
	postgres_db: str
	postgres_user: str
	postgres_password: str
	postgres_port: int

	model_config = SettingsConfigDict(
		env_file = ROOT_DIR / ".env",
		extra="ignore",
	)

settings = Settings()