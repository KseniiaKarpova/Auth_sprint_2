from uuid import UUID

from models.genre import Genre
from services.genres import GenreService, get_genre_service

from fastapi import APIRouter, Depends, Request
from exceptions import genre_not_found, genres_not_found
from core.handlers import require_access_token, JwtHandler


router = APIRouter()


@router.get(
    "/",
    response_model=list[Genre],
    response_description="Example of genres",
    summary="List of genres",
)
async def get_genres(
    request: Request,
    service: GenreService = Depends(get_genre_service),
    jwt_handler: JwtHandler = Depends(require_access_token)
) -> list[Genre]:
    genres = await service.get_data_list(url=str(request.url))
    if not genres:
        raise genres_not_found
    return genres


@router.get(
    "/{uuid}",
    response_model=Genre,
    response_description="Example of genre",
    summary="Genre",
    description="Getting genre by uuid",
)
async def get_genre_by_id(
        request: Request,
        uuid: UUID,
        service: GenreService = Depends(get_genre_service),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> Genre:
    genre = await service.get_data_by_id(url=str(request.url), id=str(uuid))
    if not genre:
        raise genre_not_found
    return genre
