import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserSession
from app.schema.user_dto import UserCreate, UserSessionCreate
from app.utils.logger import log


class UserRepository:
    """
    Repository class for CRUD operations on User and UserSession.
    Works with async SQLAlchemy sessions.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the repository with an asynchronous database session.
        :param db_session: AsyncSession instance.
        """
        self.session = db_session

    # --- User CRUD ---

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new User in the database.

        :param user_data: UserCreate schema with user info.
        :return: Created User ORM object.
        :raises: IntegrityError if uniqueness constraints fail, SQLAlchemyError for other db issues.
        """
        user = User(
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role,
            is_active=user_data.is_active,
            is_blocked=user_data.is_blocked,
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            log.error(f"Integrity error creating user: {e}")
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error creating user: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error creating user: {e}")
            raise

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        """
        Retrieve a user by their unique ID.

        :param user_id: uuid.UUID of the user.
        :return: User ORM object or None.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving user by id {user_id}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error retrieving user by id {user_id}: {e}")
            return None

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        :param email: User's email.
        :return: User ORM object or None.
        """
        try:
            stmt = select(User).where(User.email == email)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving user by email {email}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error retrieving user by email {email}: {e}")
            return None

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        :param username: User's username.
        :return: User ORM object or None.
        """
        try:
            stmt = select(User).where(User.username == username)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving user by username {username}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error retrieving user by username {username}: {e}")
            return None

    async def list_users(self, skip: int = 0, limit: int = 20) -> Sequence[User]:
        """
        List users with pagination support.

        :param skip: How many users to skip.
        :param limit: Maximum number of users to return.
        :return: List of User ORM objects.
        """
        try:
            stmt = select(User).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            log.error(f"Database error listing users: {e}")
            return []
        except Exception as e:
            log.error(f"Unknown error listing users: {e}")
            return []

    async def update_user(self, user_id: uuid.UUID, update_data: dict) -> User | None:
        """
        Update fields of a user by their ID.

        :param user_id: uuid.UUID of the user.
        :param update_data: Dictionary of fields to update.
        :return: Updated User ORM object or None if user does not exist.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return None
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error updating user {user_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error updating user {user_id}: {e}")
            raise

    async def delete_user(self, user_id: uuid.UUID) -> bool:
        """
        Delete a user from the database.

        :param user_id: uuid.UUID of the user.
        :return: True if deleted, False if user is not found.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return False
            await self.session.delete(user)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error deleting user {user_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error deleting user {user_id}: {e}")
            raise

    # --- UserSession CRUD ---

    async def create_user_session(self, session_data: UserSessionCreate) -> UserSession:
        """
        Create a new UserSession entry.

        :param session_data: UserSessionCreate schema with session info.
        :return: Created UserSession ORM object.
        :raises: IntegrityError if uniqueness constraints fail, SQLAlchemyError for other db issues.
        """
        session = UserSession(**session_data.model_dump())
        self.session.add(session)
        try:
            await self.session.commit()
            await self.session.refresh(session)
            return session
        except IntegrityError as e:
            await self.session.rollback()
            log.error(f"Integrity error creating user session: {e}")
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error creating user session: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error creating user session: {e}")
            raise

    async def get_session_by_id(self, session_id: uuid.UUID) -> UserSession | None:
        """
        Retrieve a user session by its unique ID.

        :param session_id: uuid.UUID of the session.
        :return: UserSession ORM object or None.
        """
        try:
            stmt = select(UserSession).where(UserSession.id == session_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving session by id {session_id}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error retrieving session by id {session_id}: {e}")
            return None

    async def get_sessions_by_user_id(
        self, user_id: uuid.UUID, only_active: bool = False
    ) -> Sequence[UserSession]:
        """
        Get all sessions for a user. Optionally filter for only active sessions.

        :param user_id: uuid.UUID of the user.
        :param only_active: If True, only return active sessions.
        :return: List of UserSession objects.
        """
        try:
            stmt = (
                select(UserSession)
                .where(UserSession.user_id == user_id)
                .order_by(UserSession.created_at.desc())
            )
            if only_active:
                stmt = stmt.where(UserSession.is_active.is_(True))
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving sessions for user {user_id}: {e}")
            return []
        except Exception as e:
            log.error(f"Unknown error retrieving sessions for user {user_id}: {e}")
            return []

    async def get_session_by_token(self, session_token: str) -> UserSession | None:
        """
        Retrieve a user session by its session token.

        :param session_token: The session token string.
        :return: UserSession ORM object or None if not found.
        """
        try:
            stmt = select(UserSession).where(UserSession.session_token == session_token)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(f"Database error retrieving session by token {session_token}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error retrieving session by token {session_token}: {e}")
            return None

    async def list_sessions(self, skip: int = 0, limit: int = 50) -> Sequence[UserSession]:
        """
        List all user sessions with pagination.

        :param skip: How many sessions to skip.
        :param limit: How many sessions to return.
        :return: List of UserSession ORM objects.
        """
        try:
            stmt = select(UserSession).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            log.error(f"Database error listing user sessions: {e}")
            return []
        except Exception as e:
            log.error(f"Unknown error listing user sessions: {e}")
            return []

    async def update_session(self, session_id: uuid.UUID, update_data: dict) -> UserSession | None:
        """
        Update a user session.

        :param session_id: uuid.UUID of the session.
        :param update_data: Dict of fields to update.
        :return: Updated UserSession ORM object, or None if not found.
        """
        try:
            stmt = select(UserSession).where(UserSession.id == session_id)
            result = await self.session.execute(stmt)
            session = result.scalar_one_or_none()
            if not session:
                return None
            for key, value in update_data.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            self.session.add(session)
            await self.session.commit()
            await self.session.refresh(session)
            return session
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error updating session {session_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error updating session {session_id}: {e}")
            raise

    async def delete_session(self, session_id: uuid.UUID) -> bool:
        """
        Delete a user session by ID.

        :param session_id: uuid.UUID of the session.
        :return: True if deleted, False if not found.
        """
        try:
            stmt = select(UserSession).where(UserSession.id == session_id)
            result = await self.session.execute(stmt)
            session = result.scalar_one_or_none()
            if not session:
                return False
            await self.session.delete(session)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Database error deleting session {session_id}: {e}")
            raise
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unknown error deleting session {session_id}: {e}")
            raise
