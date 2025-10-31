from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.security_settings import SecurityConfig
from app.core.settings import settings
from app.utils.security import create_access_token, decode_jwt_token, set_app_cookie


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        access_token_cookie: str = "_inteliflow_access_token",
        refresh_token_cookie: str = "_intelliflow_refresh_token",
        session_id_cookie: str = "_sid",
        public_paths: set[str] = settings.PUBLIC_ROUTES,
    ):
        super().__init__(app)
        self.ACCESS_TOKEN_COOKIE = access_token_cookie
        self.REFRESH_TOKEN_COOKIE = refresh_token_cookie
        self.SESSION_ID_COOKIE = session_id_cookie
        self.PUBLIC_PATHS = public_paths

        self.access_token_expire_minutes = SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        self.jwt_secret = SecurityConfig.SECRET_KEY
        self.jwt_algorithm = SecurityConfig.ALGORITHM

    def is_public_path(self, path: str) -> bool:
        for public_path in self.PUBLIC_PATHS:
            if path.startswith(public_path):
                return True
        return False

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        cookies = request.cookies
        access_token = cookies.get(self.ACCESS_TOKEN_COOKIE)
        refresh_token = cookies.get(self.REFRESH_TOKEN_COOKIE)
        session_id = cookies.get(self.SESSION_ID_COOKIE)
        authorized = False
        new_access_token = None

        # If all auth cookies are missing and not a public route: unauthorized
        if (not access_token and not refresh_token and not session_id) and not self.is_public_path(
            path
        ):
            return JSONResponse(
                {"detail": "Unauthorized: Missing authentication cookies."}, status_code=401
            )

        user_id = None

        if access_token:
            try:
                decoded = decode_jwt_token(
                    access_token, secret_key=self.jwt_secret, algorithms=[self.jwt_algorithm]
                )
            except Exception:
                decoded = "expired"

            # Try to refresh using refresh_token if access expired
            if decoded == "expired" and refresh_token and session_id:
                try:
                    refresh_decoded = decode_jwt_token(
                        refresh_token,
                        secret_key=self.jwt_secret,
                        algorithms=[self.jwt_algorithm],
                    )
                except Exception:
                    refresh_decoded = None

                # Check refresh_token is valid and belongs to session
                if not refresh_decoded or (
                    isinstance(refresh_decoded, dict)
                    and refresh_decoded.get("session_id") != session_id
                ):
                    return JSONResponse(
                        {"detail": "Unauthorized: invalid refresh flow."}, status_code=401
                    )
                user_id = refresh_decoded.get("sub") or refresh_decoded.get("user_id")
                if user_id:
                    new_access_token = create_access_token(str(user_id))
                    authorized = True
            elif isinstance(decoded, dict):
                user_id = decoded.get("sub") or decoded.get("user_id")
                authorized = True
        elif self.is_public_path(path):
            authorized = True
        else:
            authorized = False

        if not authorized:
            return JSONResponse({"detail": "Unauthorized."}, status_code=401)

        response = await call_next(request)

        if new_access_token:
            set_app_cookie(
                response=response,
                cookie_name=self.ACCESS_TOKEN_COOKIE,
                cookie_value=new_access_token,
                expiry=self.access_token_expire_minutes * 60,
            )

        return response
