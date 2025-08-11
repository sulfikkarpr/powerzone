from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from psycopg2.extras import RealDictCursor
from ..schemas import LoginRequest, TokenResponse
from ..db import get_db_cursor
from ..auth import verify_password, create_access_token
from jose import JWTError

router = APIRouter(tags=["auth"])
security = HTTPBearer()


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    with get_db_cursor() as cur:
        cur.execute(
            """
            SELECT id, password, role, status FROM users WHERE email = %s
            """,
            (payload.email,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_id, hashed, role, status = row
        if role != "admin":
            raise HTTPException(status_code=403, detail="Not an admin")
        if status != "active":
            raise HTTPException(status_code=403, detail="Inactive admin")
        if not verify_password(payload.password, hashed):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(str(user_id))
        return TokenResponse(access_token=token)


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    from ..auth import decode_access_token

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Verify is admin and active
    with get_db_cursor() as cur:
        cur.execute("SELECT role, status FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="User not found")
        role, status = row
        if role != "admin" or status != "active":
            raise HTTPException(status_code=403, detail="Not an active admin")
    return user_id