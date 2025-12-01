from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

# SQLAlchemy Models
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    context_used = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=5000)
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: str
    sources: List[dict] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class IndexRequest(BaseModel):
    file_path: str
    content: str
    metadata: dict = {}

class HealthResponse(BaseModel):
    status: str
    qdrant_connected: bool
    database_connected: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
