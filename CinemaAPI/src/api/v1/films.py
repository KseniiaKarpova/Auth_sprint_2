from uuid import UUID

from core.config import QueryParams, settings
from core.handlers import JwtHandler, require_access_token
from exceptions import file_not_found, film_not_found, films_not_found
from fastapi import APIRouter, Depends, Request
from models.film import Film, FilmDetail
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    "",
    response_model=list[Film],
    response_description="Example of films",
    response_model_exclude={"description", "genre", "actors", "writers", "director"},
    summary="List films",
    description="List films with pagination, "
                "genre filtration, film and rate sorting.",
)
async def get_film_list(
        film_service: FilmService = Depends(get_film_service),
        sort: str = "-imdb_rating",
        genre: str = None,
        commons: QueryParams = Depends(QueryParams),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> list[Film]:
    films = await film_service.get_data_list(sort, genre, commons.page_number, commons.page_size)
    if not films:
        raise films_not_found
    return films


@router.get(
    "/search",
    response_model=list[Film],
    response_description="Example of films",
    response_model_exclude={"description", "genre", "actors", "writers", "director", "actors_names", "writers_names"},
    description="Film searching",
    summary="List of films",
)
async def search_films(
        film_service: FilmService = Depends(get_film_service),
        query: str = "",
        commons: QueryParams = Depends(QueryParams),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> list[dict[str, Film]]:
    films = await film_service.search_data(query, commons.page_number, commons.page_size)
    if not films:
        raise films_not_found
    return films


@router.get(
    "/{film_id}",
    response_model=FilmDetail,
    response_model_exclude={"actors_names", "writers_names"},
    response_description="Example of film",
    summary="Film",
    description="Getting film by id",
)
async def get_film_details(
        request: Request,
        film_id: UUID,
        film_service: FilmService = Depends(get_film_service),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> FilmDetail:
    film = await film_service.get_data_by_id(url=str(request.url), id=str(film_id))
    if not film:
        raise film_not_found
    return film


@router.get(
    "/{film_id}/download",
    response_model=None,
    response_description="File stream response",
    summary="File stream",
    description="Getting file film by id",
)
async def download_film(
        request: Request,
        film_id: UUID,
        film_service: FilmService = Depends(get_film_service),
        jwt_handler: JwtHandler = Depends(require_access_token),
):
    film = await film_service.get_data_by_id(url=str(request.url), id=str(film_id))
    if not film:
        raise film_not_found
    file_name = film.get("file")
    if not file_name:
        raise file_not_found
    return {
        "url": f'http://{settings.file_api.full_path}/download-stream/{file_name}/'
    }
