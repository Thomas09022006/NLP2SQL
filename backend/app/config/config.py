import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field("mysql+pymysql://root:Soosai11@127.0.0.1/ipl_ai", alias="DATABASE_URL")
    gemini_api_key: str = Field("dummy_key", alias="GEMINI_API_KEY")
    jwt_secret: str = Field("super_secret_key_change_me_in_production_jwt_token_secret", alias="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Support locating .env from different nested directory depths
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
print(f"Config loaded. Connecting to database: {settings.database_url.split('@')[-1]}")
