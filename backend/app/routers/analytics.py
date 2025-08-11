from fastapi import APIRouter, Depends
from ..schemas import RevenueQuery, RevenueResponse, RevenuePoint, MemberInsights
from ..db import get_db_cursor
from .auth import get_current_admin

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/revenue", response_model=RevenueResponse)
def revenue(query: RevenueQuery, admin_id: int = Depends(get_current_admin)):
    date_trunc = "month" if query.granularity == "monthly" else "week"
    params = []
    where = []
    if query.start_date:
        where.append("due_date >= %s")
        params.append(query.start_date)
    if query.end_date:
        where.append("due_date <= %s")
        params.append(query.end_date)
    where_clause = ("WHERE " + " AND ".join(where)) if where else ""

    with get_db_cursor() as cur:
        cur.execute(
            f"""
            SELECT to_char(date_trunc('{date_trunc}', due_date), 'YYYY-MM') AS period,
                   COALESCE(SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END), 0) AS amount
            FROM payment_reminders
            {where_clause}
            GROUP BY 1
            ORDER BY 1
            """,
            params,
        )
        rows = cur.fetchall()
        points = [RevenuePoint(period=r[0], amount=float(r[1])) for r in rows]
        total = float(sum(p.amount for p in points))
        return RevenueResponse(points=points, total=total)


@router.get("/member-insights", response_model=MemberInsights)
def member_insights(admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'member' AND status = 'active'")
        active_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'member' AND status = 'inactive'")
        inactive_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM payment_reminders WHERE status = 'paid'")
        paid_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM payment_reminders WHERE status IN ('pending','sent')")
        pending_count = cur.fetchone()[0]
    return MemberInsights(
        paid_count=paid_count,
        pending_count=pending_count,
        active_count=active_count,
        inactive_count=inactive_count,
    )