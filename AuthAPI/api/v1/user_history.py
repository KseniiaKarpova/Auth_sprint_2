from core.handlers import JwtHandler, require_access_token
from fastapi import APIRouter, Depends
from schemas.user_history import UserHistory
from services.user_history import UserHistoryService, get_user_history_service

router = APIRouter()


@router.get("", response_model=list[UserHistory])
async def login_history(
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: UserHistoryService = Depends(get_user_history_service),
        ) -> list[dict[str, UserHistory]]:
    current_user = await jwt_handler.get_current_user()
    return await service.user_login_history(user_id=current_user.uuid)
