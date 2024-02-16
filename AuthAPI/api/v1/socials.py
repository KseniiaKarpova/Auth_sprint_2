from fastapi import APIRouter
from starlette.requests import Request as starler_request
from core.oauth2 import google_client
from core.config import settings

router = APIRouter()


@router.get('/')
async def main_page(request: starler_request):
    uri, state = google_client.create_authorization_url(
        url=settings.auth.google_base_url)
    return uri
