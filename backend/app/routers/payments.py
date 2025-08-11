from fastapi import APIRouter, Depends, HTTPException
from typing import List
from urllib.parse import urlencode
from datetime import date
from ..schemas import PaymentReminderCreate, PaymentReminderOut
from ..db import get_db_cursor
from .auth import get_current_admin
from ..config import settings

router = APIRouter(prefix="/payments", tags=["payments"])


def generate_upi_link(amount: float, note: str | None = None) -> str:
    params = {
        "pa": settings.upi_id or "merchant@upi",
        "pn": settings.business_name or "Gym",
        "am": f"{amount:.2f}",
        "cu": "INR",
    }
    if note:
        params["tn"] = note
    return f"upi://pay?{urlencode(params)}"


@router.post("/reminders", response_model=PaymentReminderOut)
def create_payment_reminder(payload: PaymentReminderCreate, admin_id: int = Depends(get_current_admin)):
    upi_link = generate_upi_link(payload.amount, settings.default_payment_note)
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO payment_reminders (user_id, due_date, amount, upi_link, status)
            VALUES (%s, %s, %s, %s, 'pending')
            RETURNING id, user_id, due_date, amount, upi_link, status
            """,
            (payload.user_id, payload.due_date, payload.amount, upi_link),
        )
        row = cur.fetchone()
        return PaymentReminderOut(id=row[0], user_id=row[1], due_date=row[2], amount=row[3], upi_link=row[4], status=row[5])


@router.get("/reminders/{user_id}", response_model=List[PaymentReminderOut])
def list_reminders(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id, user_id, due_date, amount, upi_link, status FROM payment_reminders WHERE user_id = %s ORDER BY due_date DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            PaymentReminderOut(id=r[0], user_id=r[1], due_date=r[2], amount=r[3], upi_link=r[4], status=r[5])
            for r in rows
        ]


@router.post("/reminders/{reminder_id}/mark-paid", response_model=PaymentReminderOut)
def mark_paid(reminder_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "UPDATE payment_reminders SET status = 'paid' WHERE id = %s RETURNING id, user_id, due_date, amount, upi_link, status",
            (reminder_id,),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Reminder not found")
        return PaymentReminderOut(id=row[0], user_id=row[1], due_date=row[2], amount=row[3], upi_link=row[4], status=row[5])