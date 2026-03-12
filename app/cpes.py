from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import CPE
from app.schemas import CPEListResponse, CPEOut, CPESearchResponse

router = APIRouter(prefix="/api/cpes", tags=["CPEs"])


@router.get("", response_model=CPEListResponse)
async def list_cpes(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * limit

    total_result = await db.execute(select(func.count()).select_from(CPE))
    total = total_result.scalar_one()

    result = await db.execute(
        select(CPE).order_by(CPE.id).offset(offset).limit(limit)
    )
    cpes = result.scalars().all()

    return CPEListResponse(
        page=page,
        limit=limit,
        total=total,
        data=[CPEOut.model_validate(c) for c in cpes],
    )


@router.get("/search", response_model=CPESearchResponse)
async def search_cpes(
    cpe_title: Optional[str] = Query(default=None),
    cpe_22_uri: Optional[str] = Query(default=None),
    cpe_23_uri: Optional[str] = Query(default=None),
    deprecation_date: Optional[date] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CPE).order_by(CPE.id)
    conditions = []

    if cpe_title:
        conditions.append(CPE.cpe_title.ilike(f"%{cpe_title}%"))
    if cpe_22_uri:
        conditions.append(CPE.cpe_22_uri.ilike(f"%{cpe_22_uri}%"))
    if cpe_23_uri:
        conditions.append(CPE.cpe_23_uri.ilike(f"%{cpe_23_uri}%"))
    if deprecation_date:
        conditions.append(
            or_(
                CPE.cpe_22_deprecation_date < deprecation_date,
                CPE.cpe_23_deprecation_date < deprecation_date,
            )
        )

    if conditions:
        from sqlalchemy import and_
        stmt = stmt.where(and_(*conditions))

    result = await db.execute(stmt)
    cpes = result.scalars().all()

    return CPESearchResponse(data=[CPEOut.model_validate(c) for c in cpes])