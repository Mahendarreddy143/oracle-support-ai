"""Chat routes"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.chat import ChatSession, ChatMessage
from app.models.issue import Issue
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate, ChatSessionResponse
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    request: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Create a new chat session"""
    # Verify issue exists if provided
    if request.issue_id:
        result = await db.execute(
            select(Issue).where(Issue.id == request.issue_id)
        )
        if not result.scalars().first():
            raise HTTPException(status_code=404, detail="Issue not found")

    session = ChatSession(
        issue_id=request.issue_id,
        user_id=current_user.id,
        title=request.title,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Get chat session"""
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return session


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: int,
    message: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Send message in chat session"""
    # Verify session
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Create message
    db_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=message.content,
        code_context=message.code_context,
    )
    db.add(db_message)
    session.message_count += 1
    await db.commit()
    await db.refresh(db_message)

    return db_message


@router.get("/sessions/{session_id}/messages")
async def get_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = 50,
):
    """Get chat history"""
    # Verify session
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalars().first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get messages
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .limit(limit)
    )
    messages = result.scalars().all()

    return {"messages": messages}
