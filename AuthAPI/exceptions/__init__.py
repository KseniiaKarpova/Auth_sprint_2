from fastapi import HTTPException, status

unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")
user_created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="User has been created")
incorrect_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")

role_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Role not found")
role_already_exist_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Role already exists")
crud_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Can`t create rules")

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")
forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")
user_updated = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

order_by_field_not_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="order by field has wrong field name")

integrity_error = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="record already exists")
