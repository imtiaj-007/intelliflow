import uuid
from typing import Optional

from jose import JWTError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.repository.user import UserRepository
from app.schema.user_dto import (
    LoginResponse,
    UserCreate,
    UserRead,
    UserSessionCreate,
    UserSessionRead,
)
from app.utils.logger import log
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)


class UserService:
    """
    Service class for handling business logic related to user management,
    authentication, and session handling.

    Provides methods to register new users, authenticate them using JWT,
    manage user sessions, and handle session revocation.
    Integrates with the UserRepository for database operations and
    handles error logging and response shaping for user-related use cases.

    Methods:
        - register_user: Register and store a new user with proper password hashing.
        - login: Authenticate user credentials and issue JWT access/refresh tokens.
        - create_session: Create a user session (for cookie/session-based auth).
        - get_active_session_by_token: Look up a session by its token and check if active.
        - revoke_session: Deactivate a session (usually on logout).
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initialize the UserService with a repository instance.

        :param user_repository: An instance of UserRepository for DB access.
        """
        self.user_repo = user_repository

    async def register_user(self, user_data: UserCreate) -> Optional[UserRead]:
        """
        Register a new user account.
        Hashes the password, attempts to store user in DB.
        If registration succeeds, returns the UserRead Pydantic object.
        On error, logs and returns None.

        :param user_data: UserCreate schema with user info.
        :return: UserRead if created, else None.
        """
        try:
            user_data.password = hash_password(user_data.password)
            user = await self.user_repo.create_user(user_data)
            return UserRead.model_validate(user, extra="ignore", from_attributes=True)
        except IntegrityError as e:
            log.error(f"User registration failed (Integrity error): {e}")
            return None
        except SQLAlchemyError as e:
            log.error(f"User registration failed (DB error): {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error during user registration: {e}")
            return None

    async def login(self, email: str, password: str) -> Optional[LoginResponse]:
        """
        Authenticate a user with JWT-based authentication and session tracking.

        If the user has an active session, return its session_id and refresh_token.
        Otherwise, create a new session and return the new details.

        :param email: User's email for lookup.
        :param password: Plaintext password for verification.
        :return: Dict with user info, access_token, refresh_token, session_id; or None if auth fails.
        """
        try:
            user = await self.user_repo.get_user_by_email(email)
            if not user:
                log.info(f"Login failed for email {email}: user not found")
                return None
            if not verify_password(password, user.password):
                log.info(f"Login failed for email {email}: bad password")
                return None
            if not user.is_active or user.is_blocked:
                log.info(f"Login rejected for email {email}: inactive or blocked")
                return None

            user_id = str(user.id)
            access_token = create_access_token(
                subject=user_id,
                extra_data={"role": str(user.role), "email": user.email},
            )

            # Try to get active session
            sessions = await self.user_repo.get_sessions_by_user_id(user_id)
            if sessions:
                session_id = str(sessions[0].id)
                refresh_token = sessions[0].session_token
            else:
                # Create a new session and its refresh token
                from uuid import uuid4

                session_id = str(uuid4())
                refresh_token = create_refresh_token(
                    subject=user_id, extra_data={"email": user.email, "session_id": session_id}
                )

                session_data = UserSessionCreate(
                    id=session_id,
                    user_id=user_id,
                    session_token=refresh_token,
                    is_active=True,
                )
                session_obj = await self.user_repo.create_user_session(session_data)
                # Use the new session
                session_id = str(session_obj.id)
                refresh_token = str(session_obj.session_token)

            return LoginResponse(
                user=UserRead.model_validate(user),
                access_token=access_token,
                refresh_token=refresh_token,
                session_id=session_id,
            )
        except JWTError as e:
            log.error(f"JWT error during login for email {email}: {e}")
            return None
        except SQLAlchemyError as e:
            log.error(f"Login failed (DB error) for email {email}: {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error during login for email {email}: {e}")
            return None

    async def create_session(self, session_data: UserSessionCreate) -> Optional[UserSessionRead]:
        """
        Create a new user session (cookie/session-based authentication).

        On success, returns a UserSessionRead Pydantic object.
        On failure, logs error and returns None.

        :param session_data: UserSessionCreate DTO containing session details.
        :return: UserSessionRead if created, else None.
        """
        try:
            session = await self.user_repo.create_user_session(session_data)
            return UserSessionRead.model_validate(session)
        except SQLAlchemyError as e:
            log.error(f"Create session failed (DB error): {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error during session creation: {e}")
            return None

    async def get_active_session_by_token(self, session_token: str) -> Optional[UserSessionRead]:
        """
        Retrieve an active session by its session token.

        Looks up the session by token, returns active session as UserSessionRead,
        or None if not found or inactive.

        :param session_token: The session token identifier.
        :return: UserSessionRead if the session is found and active; None otherwise.
        """
        try:
            session = await self.user_repo.get_session_by_token(session_token)
            if not session or not session.is_active:
                return None
            return UserSessionRead.model_validate(session)
        except SQLAlchemyError as e:
            log.error(f"Get session by token failed (DB error): {e}")
            return None
        except Exception as e:
            log.error(f"Unknown error in get_active_session_by_token: {e}")
            return None

    async def revoke_session(self, session_id: uuid.UUID) -> bool:
        """
        Deactivate (logout) a session by marking it inactive.

        Updates the session's 'is_active' field to False.
        Returns True if the session was found and updated to inactive, otherwise False.

        :param session_id: UUID of the session to revoke.
        :return: True if session marked inactive, False if not found or error.
        """
        try:
            updated_session = await self.user_repo.update_session(session_id, {"is_active": False})
            return bool(updated_session and not updated_session.is_active)
        except SQLAlchemyError as e:
            log.error(f"Revoke session failed (DB error): {e}")
            return False
        except Exception as e:
            log.error(f"Unknown error during revoke_session: {e}")
            return False
