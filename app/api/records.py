from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import date
from app import crud, schemas
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import Role
from app.services.dashboard import get_dashboard_summary

router = APIRouter()

@router.post("/", response_model=schemas.RecordOut)
async def create_record(
    record_in: schemas.RecordCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create")
    record = await crud.create_record(db, obj_in=record_in, created_by=current_user.id)
    return record

@router.get("/", response_model=List[schemas.RecordOut])
async def read_records(
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(schemas.Record).where(schemas.Record.created_by == current_user.id)
    if category:
        query = query.where(schemas.Record.category == category)
    if start_date:
        query = query.where(schemas.Record.date >= start_date)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/dashboard", response_model=schemas.DashboardOut)
async def read_dashboard(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_dashboard_summary(db, current_user.id)