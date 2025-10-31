from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import db_session_manager
from app.repository.user import UserRepository
from app.service.user import UserService


def get_user_service(session: AsyncSession = Depends(db_session_manager.get_db)) -> UserService:
    """
    Dependency function to get a UserService instance.

    Args:
        session (AsyncSession): The async database session

    Returns:
        UserService: An instance of UserService with all required dependencies
    """
    user_repo = UserRepository(db_session=session)
    return UserService(user_repository=user_repo)