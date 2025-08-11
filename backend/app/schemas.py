from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    role: str
    status: str = "active"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: str
    status: str
    join_date: datetime


class WorkoutPlanBase(BaseModel):
    user_id: int
    plan_name: str
    plan_details: dict | str
    duration_weeks: int
    created_by: int


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlanOut(BaseModel):
    id: int
    user_id: int
    plan_name: str
    plan_details: dict | str
    duration_weeks: int
    created_by: int


class MealPlanBase(BaseModel):
    user_id: int
    meal_name: str
    meal_details: dict | str
    goal: str
    created_by: int


class MealPlanCreate(MealPlanBase):
    pass


class MealPlanOut(BaseModel):
    id: int
    user_id: int
    meal_name: str
    meal_details: dict | str
    goal: str
    created_by: int


class ProgressLogBase(BaseModel):
    user_id: int
    weight: float = Field(..., ge=0)
    body_fat_percentage: float = Field(..., ge=0)
    bmi: float = Field(..., ge=0)
    log_date: datetime


class ProgressLogCreate(ProgressLogBase):
    pass


class ProgressLogUpdate(BaseModel):
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    bmi: Optional[float] = None
    log_date: Optional[datetime] = None


class ProgressLogOut(ProgressLogBase):
    id: int


class PaymentReminderBase(BaseModel):
    user_id: int
    due_date: date
    amount: float
    upi_link: Optional[str] = None
    status: str = "pending"  # pending, sent, paid


class PaymentReminderCreate(BaseModel):
    user_id: int
    due_date: date
    amount: float


class PaymentReminderOut(PaymentReminderBase):
    id: int


class SendMessageRequest(BaseModel):
    user_id: Optional[int] = None
    phone: str
    message: str


class BulkMessageRequest(BaseModel):
    phone_numbers: List[str]
    message: str


class RevenueQuery(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    granularity: str = "monthly"  # weekly | monthly


class RevenuePoint(BaseModel):
    period: str
    amount: float


class RevenueResponse(BaseModel):
    points: List[RevenuePoint]
    total: float


class MemberInsights(BaseModel):
    paid_count: int
    pending_count: int
    active_count: int
    inactive_count: int