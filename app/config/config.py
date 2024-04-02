from dotenv import load_dotenv
from pydantic import PostgresDsn
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


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    first_employee_login: str
    first_employee_password: str
    first_employee_fullname: str
    generate_test_data: bool


settings = Settings()
