from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ..schemas import UserCreate, UserUpdate, UserOut
from ..db import get_db_cursor
from .auth import get_current_admin
from ..auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (name, phone, email, password, role, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, name, phone, email, role, status, join_date
            """,
            (
                payload.name,
                payload.phone,
                payload.email,
                hash_password(payload.password),
                payload.role,
                payload.status,
            ),
        )
        row = cur.fetchone()
        return UserOut(
            id=row[0],
            name=row[1],
            phone=row[2],
            email=row[3],
            role=row[4],
            status=row[5],
            join_date=row[6],
        )


@router.get("/", response_model=List[UserOut])
def list_users(
    q: Optional[str] = Query(default=None, description="Search by name/phone/email/status"),
    status: Optional[str] = None,
    admin_id: int = Depends(get_current_admin),
):
    with get_db_cursor() as cur:
        if q:
            term = f"%{q.lower()}%"
            cur.execute(
                """
                SELECT id, name, phone, email, role, status, join_date
                FROM users
                WHERE LOWER(name) LIKE %s OR LOWER(phone) LIKE %s OR LOWER(email) LIKE %s OR LOWER(status) LIKE %s
                ORDER BY id DESC
                """,
                (term, term, term, term),
            )
        elif status:
            cur.execute(
                """
                SELECT id, name, phone, email, role, status, join_date
                FROM users WHERE status = %s ORDER BY id DESC
                """,
                (status,),
            )
        else:
            cur.execute(
                """
                SELECT id, name, phone, email, role, status, join_date
                FROM users ORDER BY id DESC
                """
            )
        rows = cur.fetchall()
        return [
            UserOut(
                id=r[0], name=r[1], phone=r[2], email=r[3], role=r[4], status=r[5], join_date=r[6]
            )
            for r in rows
        ]


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id, name, phone, email, role, status, join_date FROM users WHERE id = %s",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(
            id=row[0], name=row[1], phone=row[2], email=row[3], role=row[4], status=row[5], join_date=row[6]
        )


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, admin_id: int = Depends(get_current_admin)):
    sets = []
    values = []
    if payload.name is not None:
        sets.append("name = %s")
        values.append(payload.name)
    if payload.phone is not None:
        sets.append("phone = %s")
        values.append(payload.phone)
    if payload.email is not None:
        sets.append("email = %s")
        values.append(payload.email)
    if payload.status is not None:
        sets.append("status = %s")
        values.append(payload.status)
    if not sets:
        raise HTTPException(status_code=400, detail="Nothing to update")
    values.append(user_id)

    with get_db_cursor() as cur:
        cur.execute(f"UPDATE users SET {', '.join(sets)} WHERE id = %s RETURNING id, name, phone, email, role, status, join_date", values)
        row = cur.fetchone()
        return UserOut(id=row[0], name=row[1], phone=row[2], email=row[3], role=row[4], status=row[5], join_date=row[6])


@router.post("/{user_id}/activate", response_model=UserOut)
def activate_user(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "UPDATE users SET status = 'active' WHERE id = %s RETURNING id, name, phone, email, role, status, join_date",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(id=row[0], name=row[1], phone=row[2], email=row[3], role=row[4], status=row[5], join_date=row[6])


@router.post("/{user_id}/deactivate", response_model=UserOut)
def deactivate_user(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "UPDATE users SET status = 'inactive' WHERE id = %s RETURNING id, name, phone, email, role, status, join_date",
            (user_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(id=row[0], name=row[1], phone=row[2], email=row[3], role=row[4], status=row[5], join_date=row[6])