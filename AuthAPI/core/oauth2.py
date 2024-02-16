from authlib.integrations.starlette_client import OAuth
from core import config
from authlib.integrations.httpx_client import AsyncOAuth2Client

google_client: AsyncOAuth2Client = None
