from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
import base64

class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, username: str, password: str):
        super().__init__(app)
        self.username = username
        self.password = password

    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("authorization")

        if not auth:
            raise HTTPException(status_code=401, detail="Unauthorized")

        scheme, credentials = auth.split()
        if scheme.lower() != "basic":
            raise HTTPException(status_code=401, detail="Unauthorized")

        decoded = base64.b64decode(credentials).decode("utf-8")
        uname, pwd = decoded.split(":")

        if uname != self.username or pwd != self.password:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return await call_next(request)
