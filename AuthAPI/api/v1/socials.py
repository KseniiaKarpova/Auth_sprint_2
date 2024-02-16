from fastapi import APIRouter, Request, Query, Depends
from services.socials import SocialAccountService, get_social_service
from core.oauth2 import google_client
from core.config import settings
from schemas.auth import SocialData, UserAuthData
from models.models import SocialNetworksEnum

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
        service: SocialAccountService = Depends(get_social_service)
):
    data: dict = await google_client.fetch_token(settings.auth.google_token_url,
                                                 authorization_response=code)
    return await service.authorize(social_data=SocialData(
        user=UserAuthData(
            email=data.get('default_email'),
            name=data.get('first_name'),
            surname=data.get('last_name')
        ),
        data=data,
        social_user_id=data.get('id'),
        type=SocialNetworksEnum.Google
    )
    )
