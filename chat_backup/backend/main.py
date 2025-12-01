from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from models import ChatRequest, ChatResponse, HealthResponse, ChatSession, ChatMessage
from database import get_db, init_db, test_connection as test_db_connection
from rag_service import RAGService
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Native Book RAG Chatbot API",
    description="RAG-powered chatbot for Physical AI & Humanoid Robotics book",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "AI Native Book RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health"
        }
    }

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check system health"""
    return HealthResponse(
        status="healthy",
        qdrant_connected=rag_service.test_connection(),
        database_connected=test_db_connection(),
        timestamp=datetime.utcnow()
    )

@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint with RAG capabilities

    - **session_id**: Optional session ID for conversation continuity
    - **message**: User's question or message
    - **selected_text**: Optional text selected by user for context-aware queries
    """
    try:
        # Create or get session
        with get_db() as db:
            if request.session_id:
                try:
                    session_uuid = uuid.UUID(request.session_id)
                    session = db.query(ChatSession).filter(
                        ChatSession.id == session_uuid
                    ).first()

                    if not session:
                        session = ChatSession(id=session_uuid)
                        db.add(session)
                except ValueError:
                    # Invalid UUID, create new session
                    session = ChatSession()
                    db.add(session)
            else:
                session = ChatSession()
                db.add(session)

            db.flush()

            # Get chat history
            chat_history = db.query(ChatMessage).filter(
                ChatMessage.session_id == session.id
            ).order_by(ChatMessage.timestamp.desc()).limit(10).all()

            # Convert to message format
            history_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in reversed(chat_history)
            ]

            # Search for relevant context
            search_query = request.message
            if request.selected_text:
                search_query = f"{request.selected_text}\n\n{request.message}"

            context_docs = rag_service.search_similar(search_query, limit=5)

            # Generate response
            assistant_message = rag_service.generate_response(
                query=request.message,
                context_docs=context_docs,
                selected_text=request.selected_text,
                chat_history=history_messages
            )

            # Save user message
            user_msg = ChatMessage(
                session_id=session.id,
                role="user",
                content=request.message,
                selected_text=request.selected_text
            )
            db.add(user_msg)

            # Save assistant message
            context_used = "\n---\n".join([
                f"{doc['title'] or doc['file_path']}: {doc['content'][:200]}..."
                for doc in context_docs
            ])

            assistant_msg = ChatMessage(
                session_id=session.id,
                role="assistant",
                content=assistant_message,
                context_used=context_used
            )
            db.add(assistant_msg)

            # Update session activity
            session.last_activity = datetime.utcnow()

            db.flush()

            # Prepare response
            sources = [
                {
                    "title": doc["title"] or "Untitled",
                    "file_path": doc["file_path"],
                    "score": round(doc["score"], 3)
                }
                for doc in context_docs[:3]  # Return top 3 sources
            ]

            return ChatResponse(
                session_id=str(session.id),
                message=assistant_message,
                sources=sources,
                timestamp=datetime.utcnow()
            )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/history", tags=["Chat"])
async def get_session_history(session_id: str):
    """Get chat history for a session"""
    try:
        session_uuid = uuid.UUID(session_id)

        with get_db() as db:
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_uuid
            ).order_by(ChatMessage.timestamp.asc()).all()

            return {
                "session_id": session_id,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "selected_text": msg.selected_text,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in messages
                ]
            }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
