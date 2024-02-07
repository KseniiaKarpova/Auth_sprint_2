from fastapi import APIRouter, Depends
from services.user_history import get_user_history_service, UserHistoryService
from core.handlers import JwtHandler
from schemas.user_history import UserHistory
from core.handlers import JwtHandler, get_jwt_handler


router = APIRouter()

@router.get("", response_model=list[UserHistory])
async def login_history(
        jwt_handler: JwtHandler = Depends(get_jwt_handler),
        service : UserHistoryService = Depends(get_user_history_service),
        ) -> list[dict[str, UserHistory]]:
    current_user = await jwt_handler.get_current_user()
    return await service.user_login_history(user_id=current_user.uuid)
