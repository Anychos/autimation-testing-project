from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HttpClientSettings(BaseModel):
    base_url: HttpUrl
    timeout: int

    @property
    def url(self) -> str:
        return str(self.base_url)


class TestUserData(BaseModel):
    email: EmailStr
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore",
    )
    http_client: HttpClientSettings
    test_user: TestUserData


settings = Settings()
