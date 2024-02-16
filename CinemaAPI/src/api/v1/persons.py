from uuid import UUID

from core.config import QueryParams
from core.handlers import JwtHandler, require_access_token
from exceptions import films_not_found, person_not_found, persons_not_found
from fastapi import APIRouter, Depends, Request
from models.film import Film
from models.person import Person, PersonDetails
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[PersonDetails],
    response_description="Example of person",
    description="Person searching",
    summary="List of person",
)
async def search_person(
        request: Request,
        service: PersonService = Depends(get_person_service),
        query: str = "",
        commons: QueryParams = Depends(QueryParams),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> list[dict[str, Person]]:
    persons = await service.search_data(url=str(request.url),
                                        query=query,
                                        page_number=commons.page_number,
                                        page_size=commons.page_size)
    if not persons:
        raise persons_not_found
    return persons


@router.get(
    "/{uuid}",
    response_model=PersonDetails,
    response_description="Example of person",
    summary="Person",
    description="Getting person by uuid",
)
async def get_person_by_id(
        request: Request,
        uuid: UUID,
        service: PersonService = Depends(get_person_service),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> Person:
    person = await service.get_data_by_id(url=str(request.url), id=str(uuid))
    if not person:
        raise person_not_found
    return person


@router.get(
    "/{uuid}/film",
    response_model=list[Film],
    response_description="Example of person",
    summary="Person",
    description="Getting person by uuid",
)
async def get_films_by_person(
        request: Request,
        uuid: UUID,
        service: PersonService = Depends(get_person_service),
        jwt_handler: JwtHandler = Depends(require_access_token)
) -> list[dict[str, Film]]:
    films = await service.get_person_films(url=str(request.url), id=str(uuid))
    if not films:
        raise films_not_found
    return films
