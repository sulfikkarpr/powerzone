from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas import WorkoutPlanCreate, WorkoutPlanOut, MealPlanCreate, MealPlanOut
from ..db import get_db_cursor
from .auth import get_current_admin
import json

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/workout", response_model=WorkoutPlanOut)
def create_workout_plan(payload: WorkoutPlanCreate, admin_id: int = Depends(get_current_admin)):
    plan_details = payload.plan_details if isinstance(payload.plan_details, str) else json.dumps(payload.plan_details)
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO workout_plans (user_id, plan_name, plan_details, duration_weeks, created_by)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, plan_name, plan_details, duration_weeks, created_by
            """,
            (payload.user_id, payload.plan_name, plan_details, payload.duration_weeks, payload.created_by),
        )
        row = cur.fetchone()
        return WorkoutPlanOut(id=row[0], user_id=row[1], plan_name=row[2], plan_details=row[3], duration_weeks=row[4], created_by=row[5])


@router.get("/workout/{user_id}", response_model=List[WorkoutPlanOut])
def list_workout_plans(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id, user_id, plan_name, plan_details, duration_weeks, created_by FROM workout_plans WHERE user_id = %s ORDER BY id DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            WorkoutPlanOut(id=r[0], user_id=r[1], plan_name=r[2], plan_details=r[3], duration_weeks=r[4], created_by=r[5])
            for r in rows
        ]


@router.post("/meal", response_model=MealPlanOut)
def create_meal_plan(payload: MealPlanCreate, admin_id: int = Depends(get_current_admin)):
    meal_details = payload.meal_details if isinstance(payload.meal_details, str) else json.dumps(payload.meal_details)
    with get_db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO meal_plans (user_id, meal_name, meal_details, goal, created_by)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, meal_name, meal_details, goal, created_by
            """,
            (payload.user_id, payload.meal_name, meal_details, payload.goal, payload.created_by),
        )
        row = cur.fetchone()
        return MealPlanOut(id=row[0], user_id=row[1], meal_name=row[2], meal_details=row[3], goal=row[4], created_by=row[5])


@router.get("/meal/{user_id}", response_model=List[MealPlanOut])
def list_meal_plans(user_id: int, admin_id: int = Depends(get_current_admin)):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT id, user_id, meal_name, meal_details, goal, created_by FROM meal_plans WHERE user_id = %s ORDER BY id DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        return [
            MealPlanOut(id=r[0], user_id=r[1], meal_name=r[2], meal_details=r[3], goal=r[4], created_by=r[5])
            for r in rows
        ]