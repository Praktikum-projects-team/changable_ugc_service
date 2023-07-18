import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    is_debug: bool = Field(..., env='IS_DEBUG')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')


class MongoConfig(BaseSettings):
    host: str = Field(..., env='MONGO_HOST')
    port: int = Field(..., env='MONGO_PORT')
    db_name: str = Field(..., env='MONGO_DB_NAME')


app_config = AppConfig()
auth_config = AuthConfig()
mongo_config = MongoConfig()
