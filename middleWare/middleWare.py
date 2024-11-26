from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = FastAPI()

# Configuración de seguridad para Swagger UI
bearer_scheme = HTTPBearer()
class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)  # No verificar JWT en preflight
        if request.url.path.startswith("/api/protected"):
            authorization: str = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer"):
                return JSONResponse(
                    {"detail": "Authorization header missing or invalid"},
                    status_code=401
                )
            try:
                token = authorization.split(" ")[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = payload
            except jwt.ExpiredSignatureError:
                return JSONResponse({"detail": "Token has expired"}, status_code=401)
            except jwt.InvalidTokenError:
                return JSONResponse({"detail": "Invalid token"}, status_code=401)
        return await call_next(request)

app.add_middleware(JWTMiddleware)