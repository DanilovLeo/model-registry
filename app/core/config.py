from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    postgres_user: str = "modelregistry"
    postgres_password: str = "changeme"
    postgres_db: str = "modelregistry"
    postgres_host: str = "db"
    postgres_port: int = 5432

    database_url: str = ""

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True

    legacy_models_path: str = "/app/models"

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
