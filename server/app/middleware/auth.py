from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.security_settings import SecurityConfig
from app.core.settings import settings
from app.utils.security import create_access_token, set_app_cookie, verify_jwt_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        access_token_cookie: str = "_intelliflow_access_token",
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
            if path == public_path:
                return True
        return False

    def is_preflight_or_head_method(self, method: str) -> bool:
        return method.upper() in {"OPTIONS", "HEAD"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        # Allow public paths immediately
        if self.is_public_path(path) or self.is_preflight_or_head_method(method):
            return await call_next(request)

        cookies = request.cookies
        access_token = cookies.get(self.ACCESS_TOKEN_COOKIE)
        refresh_token = cookies.get(self.REFRESH_TOKEN_COOKIE)
        session_id = cookies.get(self.SESSION_ID_COOKIE)
        authorized = False
        new_access_token = None
        user_id = None

        # If all auth cookies are missing: unauthorized
        if not access_token and not refresh_token and not session_id:
            return JSONResponse(
                {"detail": "Unauthorized: Missing authentication cookies."}, status_code=401
            )

        # Case 1: No access token but have refresh token and session ID
        if not access_token and refresh_token and session_id:
            refresh_decoded = self._decode_token(refresh_token, refresh=True)
            if refresh_decoded and refresh_decoded.get("session_id") == session_id:
                user_id = refresh_decoded.get("sub") or refresh_decoded.get("user_id")
                if user_id:
                    new_access_token = create_access_token(str(user_id))
                    authorized = True
            else:
                return JSONResponse(
                    {"detail": "Unauthorized: Invalid refresh token or session."}, status_code=401
                )

        # Case 2: Have access token
        elif access_token:
            decoded = self._decode_token(access_token)

            # Access token is valid
            if decoded and decoded != "expired":
                user_id = decoded.get("sub") or decoded.get("user_id")
                if user_id:
                    authorized = True

            # Access token expired, try refresh
            elif decoded == "expired" and refresh_token and session_id:
                refresh_decoded = self._decode_token(refresh_token, refresh=True)

                if refresh_decoded and refresh_decoded.get("session_id") == session_id:
                    user_id = refresh_decoded.get("sub") or refresh_decoded.get("user_id")
                    if user_id:
                        new_access_token = create_access_token(str(user_id))
                        authorized = True
                else:
                    return JSONResponse(
                        {"detail": "Unauthorized: Invalid refresh token or session."},
                        status_code=401,
                    )
            else:
                # Access token invalid/expired and no valid refresh path
                return JSONResponse(
                    {"detail": "Unauthorized: Invalid or expired token."}, status_code=401
                )

        if not authorized:
            return JSONResponse({"detail": "Unauthorized."}, status_code=401)

        # Add user_id to request state
        if user_id:
            request.state.user_id = user_id
            headers = list(request.scope["headers"])
            headers.append((b"x-user-id", str(user_id).encode()))
            request.scope["headers"] = headers

        response = await call_next(request)

        # Set new access token cookie if refreshed
        if new_access_token:
            set_app_cookie(
                response=response,
                cookie_name=self.ACCESS_TOKEN_COOKIE,
                cookie_value=new_access_token,
                expiry=self.access_token_expire_minutes * 60,
            )

        return response

    def _decode_token(self, token: str, refresh: bool = False):
        """Helper method to decode JWT tokens with consistent error handling."""
        try:
            return verify_jwt_token(token, refresh)
        except Exception:
            return None
