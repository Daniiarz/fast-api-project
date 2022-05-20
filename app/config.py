from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str = "postgresql://test:test@127.0.0.1:5445/test"
    redis_url: str = 'redis://localhost:6336/1'

    # JWT Configs
    secret_key: str
    jwt_algorithm: str = 'HS256'
    access_token_expire_days: int = 3

    class Config:
        env_file = '../local.env'
        env_file_encoding = 'utf-8'


settings = Settings()
