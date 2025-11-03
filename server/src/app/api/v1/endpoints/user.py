import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.v1.deps import get_user_service
from app.schema.user_dto import UserCreate, UserLogin, UserRead
from app.service.user import UserService
from app.utils.security import set_app_cookie

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    Register a new user in the system.

    This endpoint creates a new user account with the provided user data.
    The user will be created with default settings and status.

    Args:
        user_data (UserCreate): The user registration data containing:
            - email: User's email address (must be unique)
            - password: User's password (will be hashed)
            - first_name: User's first name
            - last_name: User's last name
        user_service (UserService): Injected user service dependency

    Returns:
        UserRead: The created user object with user details

    Raises:
        HTTPException:
            - 400: If registration fails (duplicate email or invalid input)
            - 500: If internal server error occurs during registration
    """
    user = await user_service.register_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed (possibly duplicate or bad input)",
        )
    return user


@router.post("/login")
async def login_user(
    response: Response,
    body: UserLogin,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    Authenticate user and create session with access and refresh tokens.

    This endpoint validates user credentials and upon successful authentication,
    sets HTTP-only cookies for access token, refresh token, and session ID.

    Args:
        response (Response): FastAPI response object for setting cookies
        body (UserLogin): User login credentials containing:
            - email: User's registered email address
            - password: User's password for authentication
        user_service (UserService): Injected user service dependency

    Returns:
        UserRead: The authenticated user object with user details

    Raises:
        HTTPException:
            - 422: If email or password fields are missing
            - 401: If credentials are invalid or user is blocked/inactive
            - 500: If internal server error occurs during authentication
    """
    if not body.email or not body.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Email and password required."
        )

    auth_result = await user_service.login(email=body.email, password=body.password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or user blocked/inactive",
        )

    set_app_cookie(
        response=response,
        cookie_name="_intelliflow_access_token",
        cookie_value=auth_result.access_token,
    )
    set_app_cookie(
        response=response,
        cookie_name="_intelliflow_refresh_token",
        cookie_value=auth_result.refresh_token,
        expiry=604800,  # 7 Days: 7 * 24 * 60 * 60
    )
    set_app_cookie(
        response=response,
        cookie_name="_sid",
        cookie_value=auth_result.session_id,
        expiry=604800,  # 7 Days: 7 * 24 * 60 * 60
    )
    return auth_result.user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    Retrieve user details by user ID.

    This endpoint fetches user information for the specified user ID.
    Only returns active users that exist in the system.

    Args:
        user_id (uuid.UUID): The unique identifier of the user to retrieve
        user_service (UserService): Injected user service dependency

    Returns:
        UserRead: The user object with complete user details

    Raises:
        HTTPException:
            - 404: If no user is found with the specified ID
            - 500: If internal server error occurs during retrieval
    """
    user = await user_service.user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(user)
