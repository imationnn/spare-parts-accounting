from datetime import timedelta

from dotenv import load_dotenv
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


load_dotenv()


class PGConfig(BaseSettings):
    host: str
    port: int
    name: str
    login: str | None = None
    password: str | None = None
    scheme: str
    echo: bool

    @property
    def pg_dsn(self):
        pg_dsn: str = PostgresDsn.build(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            username=self.login,
            password=self.password,
            path=self.name
        ).unicode_string()
        return pg_dsn


class AuthConfig(BaseSettings):
    minutes: int = Field(alias='access_token_exp_minutes')
    hours: int = Field(alias='refresh_token_exp_hours')
    algorithm: str
    secret_key: str

    @property
    def access_token_exp(self):
        return timedelta(minutes=self.minutes)

    @property
    def refresh_token_exp(self):
        return timedelta(hours=self.hours)


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    first_employee_login: str
    first_employee_password: str
    first_employee_fullname: str
    generate_test_data: bool


settings = Settings()
auth_config = AuthConfig()
