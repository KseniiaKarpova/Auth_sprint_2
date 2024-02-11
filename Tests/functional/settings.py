from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    service_url: str = Field('http://test_auth_api:9999', env='SERVICE_URL')


test_settings = TestSettings()
