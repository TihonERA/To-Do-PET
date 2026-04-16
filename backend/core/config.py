from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=r"C:\Users\User\Documents\To-Do-PET\.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()