from pydantic import MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_dsn: MongoDsn
    mongodb_database_name: str
