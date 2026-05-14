"""Search routes"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, or_

from app.database import get_db
from app.models.issue import Issue

router = APIRouter()


@router.get("/issues")
async def search_issues(
    q: str = Query(..., min_length=3),
    category: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, le=50),
    offset: int = Query(0),
):
    """Search issues by keyword"""
    query = select(Issue).where(
        or_(
            Issue.title.ilike(f"%{q}%"),
            Issue.description.ilike(f"%{q}%"),
            Issue.error_code.ilike(f"%{q}%"),
        )
    )

    if category:
        query = query.where(Issue.category == category)

    # Count total
    count_result = await db.execute(
        select(func.count()).select_from(Issue).where(
            or_(
                Issue.title.ilike(f"%{q}%"),
                Issue.description.ilike(f"%{q}%"),
            )
        )
    )
    total = count_result.scalar()

    # Get results
    query = query.order_by(desc(Issue.upvote_count)).offset(offset).limit(limit)
    result = await db.execute(query)
    issues = result.scalars().all()

    return {
        "query": q,
        "results": issues,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
