from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas import ProgressLogCreate, ProgressLogUpdate, ProgressLogOut
from ..db import get_db_cursor
from .auth import get_current_admin

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/", response_model=ProgressLogOut)
def create_progress(payload: ProgressLogCreate, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO progress_logs (user_id, weight, body_fat_percentage, bmi, log_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, weight, body_fat_percentage, bmi, log_date
            """,
            (payload.user_id, payload.weight, payload.body_fat_percentage, payload.bmi, payload.log_date),
        )
        row = cur.fetchone()
        return ProgressLogOut(id=row[0], user_id=row[1], weight=row[2], body_fat_percentage=row[3], bmi=row[4], log_date=row[5])


@router.get("/{user_id}", response_model=List[ProgressLogOut])
def list_progress(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id, user_id, weight, body_fat_percentage, bmi, log_date FROM progress_logs WHERE user_id = %s ORDER BY log_date DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            ProgressLogOut(id=r[0], user_id=r[1], weight=r[2], body_fat_percentage=r[3], bmi=r[4], log_date=r[5])
            for r in rows
        ]


@router.put("/{log_id}", response_model=ProgressLogOut)
def update_progress(log_id: int, payload: ProgressLogUpdate, admin_id: int = Depends(get_current_admin)):
    sets = []
    values = []
    if payload.weight is not None:
        sets.append("weight = %s")
        values.append(payload.weight)
    if payload.body_fat_percentage is not None:
        sets.append("body_fat_percentage = %s")
        values.append(payload.body_fat_percentage)
    if payload.bmi is not None:
        sets.append("bmi = %s")
        values.append(payload.bmi)
    if payload.log_date is not None:
        sets.append("log_date = %s")
        values.append(payload.log_date)
    if not sets:
        raise HTTPException(status_code=400, detail="Nothing to update")
    values.append(log_id)

    with get_db_cursor() as cur:
        cur.execute(
            f"UPDATE progress_logs SET {', '.join(sets)} WHERE id = %s RETURNING id, user_id, weight, body_fat_percentage, bmi, log_date",
            values,
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Log not found")
        return ProgressLogOut(id=row[0], user_id=row[1], weight=row[2], body_fat_percentage=row[3], bmi=row[4], log_date=row[5])


@router.delete("/{log_id}")
def delete_progress(log_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute("DELETE FROM progress_logs WHERE id = %s", (log_id,))
    return {"ok": True}