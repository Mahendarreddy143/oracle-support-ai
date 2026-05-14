"""Issues routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func

from app.database import get_db
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueResponse, IssueListResponse
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/", response_model=IssueResponse)
async def create_issue(
    issue: IssueCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Create a new issue"""
    db_issue = Issue(
        **issue.dict(),
        created_by=current_user.id,
    )
    db.add(db_issue)
    await db.commit()
    await db.refresh(db_issue)
    return db_issue


@router.get("/", response_model=IssueListResponse)
async def list_issues(
    db: AsyncSession = Depends(get_db),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
):
    """List all issues with filters"""
    query = select(Issue)

    if category:
        query = query.where(Issue.category == category)
    if status:
        query = query.where(Issue.status == status)
    if severity:
        query = query.where(Issue.severity == severity)

    # Get total count
    count_result = await db.execute(select(func.count()).select_from(Issue))
    total = count_result.scalar()

    # Get paginated results
    query = query.order_by(desc(Issue.created_at)).offset(offset).limit(limit)
    result = await db.execute(query)
    issues = result.scalars().all()

    return IssueListResponse(
        data=issues,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(issue_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific issue"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    issue = result.scalars().first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Increment view count
    issue.view_count += 1
    await db.commit()

    return issue


@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: int,
    issue_update: IssueCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Update issue"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    db_issue = result.scalars().first()

    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if db_issue.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update fields
    for key, value in issue_update.dict(exclude_unset=True).items():
        setattr(db_issue, key, value)

    await db.commit()
    await db.refresh(db_issue)
    return db_issue


@router.delete("/{issue_id}")
async def delete_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Delete issue"""
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    db_issue = result.scalars().first()

    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if db_issue.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.delete(db_issue)
    await db.commit()

    return {"message": "Issue deleted"}
