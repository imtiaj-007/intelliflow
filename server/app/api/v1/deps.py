import uuid

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embedding_manager import EmbeddingInstance
from app.aws.s3_manager import S3Instance
from app.db.session import db_session_manager
from app.repository.file import FileRepository
from app.repository.user import UserRepository
from app.repository.workflow import WorkflowRepository
from app.service.chat import ChatService
from app.service.file import FileService
from app.service.user import UserService
from app.service.workflow import WorkflowService


def get_current_user(request: Request) -> uuid.UUID:
    """
    Dependency function to get the current user from the request headers.
    """
    user_id = request.headers.get("x-user-id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Missing user ID."
        )
    return uuid.UUID(user_id)


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


def get_file_service(session: AsyncSession = Depends(db_session_manager.get_db)) -> FileService:
    """
    Dependency function to get a FileService instance.

    Args:
        session (AsyncSession): The async database session

    Returns:
        FileService: An instance of FileService with all required dependencies
    """
    s3_manager = S3Instance.get_s3_manager()
    embedding_manager = EmbeddingInstance.get_instance()
    file_repo = FileRepository(db_session=session)
    return FileService(
        s3_manager=s3_manager, embedding_manager=embedding_manager, file_repository=file_repo
    )


def get_workflow_service(
    session: AsyncSession = Depends(db_session_manager.get_db),
) -> WorkflowService:
    """
    Dependency function to get a WorkflowService instance.

    Args:
        session (AsyncSession): The async database session

    Returns:
        WorkflowService: An instance of WorkflowService with all required dependencies
    """
    file_repo = FileRepository(db_session=session)
    workflow_repo = WorkflowRepository(db_session=session)
    return WorkflowService(workflow_repository=workflow_repo, file_repository=file_repo)


def get_chat_service(
    session: AsyncSession = Depends(db_session_manager.get_db),
) -> ChatService:
    """
    Dependency function to get a ChatService instance.

    Args:
        session (AsyncSession): The async database session

    Returns:
        ChatService: An instance of ChatService with all required dependencies
    """
    file_repo = FileRepository(db_session=session)
    return ChatService(file_repository=file_repo)
