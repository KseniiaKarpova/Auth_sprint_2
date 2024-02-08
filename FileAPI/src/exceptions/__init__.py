from http import HTTPStatus

from fastapi import HTTPException

file_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="File Not Found")
server_error = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.NOT_FOUND, detail="sorry... some problem")
file_already_exist_error = HTTPException(status_code=HTTPStatus.CONFLICT, detail="File with that name already exists")
