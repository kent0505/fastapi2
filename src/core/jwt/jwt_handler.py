from fastapi          import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.core.config  import settings
import bcrypt
import jwt


def signJWT(id: int, role: str):
    encoded = jwt.encode(
        key       = settings.jwt_key,
        algorithm = settings.jwt_algorithm,
        payload   = {
            "id":     id, 
            "role":   role, 
            "expiry": settings.jwt_expiry
        }, 
    )
    return encoded


def decodeJWT(token: str):
    decoded = jwt.decode(
        jwt        = token, 
        key        = settings.jwt_key, 
        algorithms = [settings.jwt_algorithm]
    )
    return decoded


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
    return hashed


def check_password(password1: str, password2: str):
    try:
        hashed = bcrypt.checkpw(password1.encode("utf-8"), password2.encode("utf-8"))
        return hashed
    except:
        return False


def verify_jwt(token: str) -> bool:
    try:
        payload = decodeJWT(token)
    except:
        return False
    return payload["role"] == "admin"


class JwtAdmin(HTTPBearer):
    def __init__(self, auto_Error: bool=True):
        super(JwtAdmin, self).__init__(auto_error=auto_Error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JwtAdmin, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="invalid authorization code")
    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decodeJWT(token)
        except:
            payload = None
        if payload is None or "role" not in payload:
            return False
        return payload["role"] == "admin"


class JwtCustomer(HTTPBearer):
    def __init__(self, auto_Error: bool=True):
        super(JwtCustomer, self).__init__(auto_error=auto_Error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JwtCustomer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="invalid authorization code")
    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decodeJWT(token)
        except:
            payload = None
        if payload is None or "role" not in payload:
            return False
        return payload["role"] == "customer"