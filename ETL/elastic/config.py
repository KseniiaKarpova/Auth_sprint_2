from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ElasticSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='es_')

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


settings = ElasticSettings()
