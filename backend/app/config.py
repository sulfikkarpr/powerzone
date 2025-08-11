from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "Powerzone Backend"
    api_prefix: str = "/api"
    cors_origins: List[str] | str = "*"

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    # DB
    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    # WhatsApp Cloud API
    whatsapp_token: str | None = None
    whatsapp_phone_number_id: str | None = None

    # UPI
    upi_id: str | None = None
    business_name: str | None = None
    default_payment_note: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()