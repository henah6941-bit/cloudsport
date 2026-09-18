from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    api_sports_key: str | None = None
    api_sports_base_url: str = "https://v3.football.api-sports.io"
    api_sports_timeout_seconds: float = 10
    cors_origins: str = "http://localhost:5173"
    prediction_provider: str = "rules"
    anthropic_api_key: str | None = None
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

settings = Settings()
