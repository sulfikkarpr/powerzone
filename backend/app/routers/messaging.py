from fastapi import APIRouter, Depends, HTTPException
from typing import List
import requests
from ..schemas import SendMessageRequest, BulkMessageRequest
from ..config import settings
from .auth import get_current_admin

router = APIRouter(prefix="/messaging", tags=["messaging"])


def send_whatsapp_text(phone: str, message: str) -> dict:
    if not settings.whatsapp_token or not settings.whatsapp_phone_number_id:
        raise HTTPException(status_code=500, detail="WhatsApp API not configured")
    url = f"https://graph.facebook.com/v20.0/{settings.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    if not resp.ok:
        raise HTTPException(status_code=502, detail=f"WhatsApp API error: {resp.text}")
    return resp.json()


@router.post("/send")
def send_message(payload: SendMessageRequest, admin_id: int = Depends(get_current_admin)):
    result = send_whatsapp_text(payload.phone, payload.message)
    return {"ok": True, "result": result}


@router.post("/send-bulk")
def send_bulk(payload: BulkMessageRequest, admin_id: int = Depends(get_current_admin)):
    results: List[dict] = []
    for phone in payload.phone_numbers:
        try:
            results.append({"phone": phone, "result": send_whatsapp_text(phone, payload.message)})
        except HTTPException as e:
            results.append({"phone": phone, "error": str(e.detail)})
    return {"ok": True, "results": results}