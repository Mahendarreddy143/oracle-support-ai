"""Analytics routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from datetime import datetime, timedelta

from app.database import get_db
from app.models.issue import Issue
from app.models.user import User

router = APIRouter()


@router.get("/stats")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Get overall statistics"""
    # Total issues
    total_issues = await db.execute(select(func.count(Issue.id)))
    total = total_issues.scalar()

    # Resolved issues
    resolved = await db.execute(
        select(func.count(Issue.id)).where(Issue.status == "resolved")
    )
    resolved_count = resolved.scalar()

    # Active users
    users = await db.execute(select(func.count(distinct(User.id))))
    user_count = users.scalar()

    return {
        "total_issues": total,
        "resolved_issues": resolved_count,
        "active_users": user_count,
        "resolution_rate": (resolved_count / total * 100) if total > 0 else 0,
    }


@router.get("/categories")
async def get_category_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics by category"""
    result = await db.execute(
        select(
            Issue.category,
            func.count(Issue.id).label("total"),
            func.count(
                Issue.id.filter(Issue.status == "resolved")
            ).label("resolved"),
        )
        .group_by(Issue.category)
    )
    rows = result.all()

    categories = {}
    for row in rows:
        categories[row[0]] = {"total": row[1], "resolved": row[2]}

    return categories
