from http import HTTPStatus

from fastapi import HTTPException

genres_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres Not Found")
genre_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre Not Found")

films_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
film_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")

person_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person Not Found")
persons_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Persons Not Found")

file_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="File Not Found")
forbidden_error = HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You have been denied access")
server_error = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="ooops")
