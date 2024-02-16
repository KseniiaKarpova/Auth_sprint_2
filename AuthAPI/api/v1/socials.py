from fastapi import APIRouter, Request, Query
from starlette.requests import Request as starler_request
from core.oauth2 import google_client
from core.config import settings

router = APIRouter()


@router.get('/')
async def main_page(
        request: Request):
    uri, state = google_client.create_authorization_url(
        url=settings.auth.google_base_url)
    return uri


@router.route('/auth')
async def auth2(
        request: Request,
        code: str = Query(description='Code from auth provider'),
    ):
    data = await google_client.fetch_token(settings.auth.google_token_url
                                    ,authorization_response=code)
    return data
