"""
FastAPI backend for RAG Pipeline
Provides REST API endpoints for chat and document retrieval
"""

import pickle
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.llm.llm_service import LLMService

# ====== Models ======
class ChatMessage(BaseModel):
    message: str
    document_filter: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    document_mentioned: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    qdrant_connected: bool


# ====== Global State ======
class RAGState:
    embedding_service: Optional[EmbeddingService] = None
    qdrant_store: Optional[QdrantStore] = None
    llm_service: Optional[LLMService] = None
    document_store: Optional[dict] = None


state = RAGState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Loading RAG services...")
    try:
        state.embedding_service = EmbeddingService()
        state.qdrant_store = QdrantStore()
        state.llm_service = LLMService()

        # Load document store
        with open("app/storage/document_store.pkl", "rb") as f:
            state.document_store = pickle.load(f)

        print(f"✅ Loaded {len(state.document_store)} documents")
        print("✅ RAG pipeline ready!")
    except Exception as e:
        print(f"❌ Error loading services: {e}")
        raise

    yield

    # Shutdown
    print("🛑 Shutting down RAG services...")


# ====== FastAPI App ======
app = FastAPI(
    title="RAG Chat API",
    description="REST API for Retrieval-Augmented Generation chatbot",
    version="1.0.0",
    lifespan=lifespan,
)

# ====== CORS Middleware ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====== Endpoints ======
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        models_loaded=state.embedding_service is not None,
        qdrant_connected=state.qdrant_store.health_check() if state.qdrant_store else False,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(chat_msg: ChatMessage):
    """
    Chat endpoint for RAG queries
    
    Args:
        message: User question/message
        document_filter: Optional document filename to search within
    
    Returns:
        ChatResponse with answer and sources
    """
    if not state.embedding_service or not state.qdrant_store or not state.llm_service:
        raise HTTPException(status_code=503, detail="RAG services not initialized")

    try:
        question = chat_msg.message.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        matched_file = None
        
        # ====== Check if document is mentioned or filtered ======
        if chat_msg.document_filter:
            matched_file = chat_msg.document_filter
        else:
            for file_name in state.document_store.keys():
                if file_name.lower() in question.lower():
                    matched_file = file_name
                    break

        sources = []

        # ====== Document Summary Mode ======
        if matched_file:
            if matched_file not in state.document_store:
                raise HTTPException(status_code=404, detail=f"Document '{matched_file}' not found")

            chunks = state.document_store[matched_file]
            context = "\n\n".join(chunk.text for chunk in chunks)

            # Store sources
            for chunk in chunks[:3]:  # Top 3 chunks
                sources.append({
                    "document": matched_file,
                    "text": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                    "metadata": chunk.metadata,
                })

            answer = state.llm_service.generate(context, question)

        # ====== Normal RAG Search ======
        else:
            # Generate query embedding
            query_embedding = state.embedding_service.embed([question])[0]

            # Search Qdrant
            chunks = state.qdrant_store.search(query_embedding, k=5)

            # Build context
            context = "\n\n".join(chunk.text for chunk in chunks)

            # Store sources
            for chunk in chunks[:3]:  # Top 3 sources
                sources.append({
                    "document": chunk.metadata.get("file_name", "Unknown"),
                    "text": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                    "metadata": chunk.metadata,
                })

            # Generate answer
            answer = state.llm_service.generate(context, question)

        return ChatResponse(
            answer=answer,
            sources=sources,
            document_mentioned=matched_file,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/documents")
async def get_documents():
    """Get list of indexed documents"""
    if not state.document_store:
        raise HTTPException(status_code=503, detail="Document store not initialized")

    documents = []
    for file_name, chunks in state.document_store.items():
        documents.append({
            "name": file_name,
            "chunk_count": len(chunks),
        })

    return {
        "total": len(documents),
        "documents": documents,
    }


@app.get("/stats")
async def get_stats():
    """Get RAG pipeline statistics"""
    if not state.document_store or not state.qdrant_store:
        raise HTTPException(status_code=503, detail="Services not initialized")

    total_chunks = sum(len(chunks) for chunks in state.document_store.values())
    
    try:
        collection_info = state.qdrant_store.get_collection_info()
    except Exception as e:
        collection_info = {"error": str(e)}

    return {
        "documents": len(state.document_store),
        "total_chunks": total_chunks,
        "qdrant_collection": collection_info,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
