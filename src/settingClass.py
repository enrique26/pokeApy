from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POKEURL_BASE: str
    API_BERRIES: str
    OFFSET_BERRIES: int
    LIMIT_BERRIES: int

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()

baseurl = settings.POKEURL_BASE
apiBerries = settings.API_BERRIES
offsetBerries = settings.OFFSET_BERRIES
limitBerries = settings.LIMIT_BERRIES