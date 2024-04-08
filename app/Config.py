from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_username : str
    database_password : str
    database_name : str
    database_hostname : str
    database_port: str
    database_secretkey :str
    algorithm : str
    SECRET_CODE_EXPIRATION_IN_MINUTES : int
    class Config:
        env_file = ".env"



settings = Settings()