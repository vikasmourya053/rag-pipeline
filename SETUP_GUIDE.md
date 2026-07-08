# RAG ChatBot - Setup & Running Guide

## 🎯 Overview

This project combines a FastAPI backend with a Next.js frontend to create a ChatGPT-like interface for querying your documents using a Retrieval-Augmented Generation (RAG) pipeline.

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      Next.js Frontend (Port 3000)    │
│  - ChatGPT-like UI                  │
│  - Message management               │
│  - Document sidebar                 │
└─────────────────┬───────────────────┘
                  │ HTTP
┌─────────────────▼───────────────────┐
│    FastAPI Backend (Port 8000)       │
│  - /chat endpoint                   │
│  - /documents endpoint              │
│  - /stats endpoint                  │
│  - RAG pipeline integration         │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   RAG Services                      │
│  - Embeddings (Sentence Transformers)│
│  - Vector Store (Qdrant)            │
│  - LLM Service                      │
│  - Document Store                   │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Qdrant)
- Qdrant running on `localhost:6333`

## 🚀 Quick Start

### 1. Backend Setup

#### Step 1: Ensure Qdrant is running

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Access Qdrant dashboard: http://localhost:6333/dashboard

#### Step 2: Start FastAPI server

```bash
cd d:\go\rag-pipeline
$env:PYTHONPATH = "."; python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs** (interactive Swagger UI)

### 2. Frontend Setup

#### Step 1: Navigate to chatbot directory

```bash
cd d:\go\rag-pipeline\chatbot
```

#### Step 2: Install dependencies

```bash
npm install
```

#### Step 3: Start the Next.js dev server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## 🌐 API Endpoints

### Chat Endpoint
- **POST** `/chat`
- **Request Body:**
  ```json
  {
    "message": "What is AI?",
    "document_filter": "ai.pdf"  // Optional
  }
  ```
- **Response:**
  ```json
  {
    "answer": "AI stands for Artificial Intelligence...",
    "sources": [
      {
        "document": "ai.pdf",
        "text": "AI is...",
        "metadata": {...}
      }
    ],
    "document_mentioned": "ai.pdf"
  }
  ```

### Documents Endpoint
- **GET** `/documents`
- **Response:**
  ```json
  {
    "total": 5,
    "documents": [
      {
        "name": "ai.pdf",
        "chunk_count": 150
      }
    ]
  }
  ```

### Health Check
- **GET** `/health`
- **Response:**
  ```json
  {
    "status": "healthy",
    "models_loaded": true,
    "qdrant_connected": true
  }
  ```

### Statistics
- **GET** `/stats`
- **Response:**
  ```json
  {
    "documents": 5,
    "total_chunks": 2542,
    "qdrant_collection": {
      "name": "rag_documents",
      "points_count": 2542
    }
  }
  ```

## 🎨 Frontend Features

### Chat Interface
- **Message history** - Persistent conversation display
- **Source attribution** - View documents used for answers
- **Real-time typing indicator** - Visual feedback during processing
- **Auto-scrolling** - Automatically scroll to latest messages

### Sidebar
- **Document browser** - Select specific documents to search
- **Search all documents** - Global search across all indexed content
- **New chat button** - Clear conversation and start fresh
- **Document statistics** - View chunk count per document

### Features
- ✅ Message auto-formatting
- ✅ Multi-line input support (Shift+Enter)
- ✅ Responsive design (desktop & mobile)
- ✅ Error handling with fallback messages
- ✅ Loading states and animations

## 📱 Usage

### 1. Start everything in order:

**Terminal 1 - Qdrant:**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Terminal 2 - FastAPI Backend:**
```bash
cd d:\go\rag-pipeline
$env:PYTHONPATH = "."; python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - Next.js Frontend:**
```bash
cd d:\go\rag-pipeline\chatbot
npm run dev
```

### 2. Open in browser:

Navigate to: **http://localhost:3000**

### 3. Start chatting:

1. Select a document from the sidebar or search all documents
2. Type your question in the input field
3. Press `Enter` to send (or `Shift+Enter` for new line)
4. View the response with source attribution

## 🔧 Configuration

### Backend Configuration
- **`QDRANT_URL`**: Qdrant server URL (default: `http://localhost:6333`)
- **`QDRANT_COLLECTION_NAME`**: Collection name (default: `rag_documents`)
- **`EMBEDDING_MODEL`**: Embedding model (default: `all-MiniLM-L6-v2`)
- **`LLM_URL`**: LLM API endpoint

Edit `app/config.py` to modify settings.

### Frontend Configuration
- **`NEXT_PUBLIC_API_URL`**: Backend API URL (default: `http://localhost:8000`)

Edit `chatbot/.env.local` to modify settings.

## 🛠️ Development

### Backend Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Frontend Development

- Hot reloading enabled
- TypeScript support
- CSS modules for component styling
- Responsive design with mobile-first approach

## 📦 Dependencies

### Backend
- FastAPI - Web framework
- Uvicorn - ASGI server
- Qdrant-client - Vector DB client
- Sentence-transformers - Embeddings
- PyPDF - PDF processing

### Frontend
- Next.js 14+ - React framework
- TypeScript - Type safety
- CSS modules - Component styling

## 🐛 Troubleshooting

### Connection Refused (Port 8000)
```bash
# Check if API is running
curl http://localhost:8000/health

# Restart the API server
$env:PYTHONPATH = "."; python -m uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

### Qdrant Connection Error
```bash
# Ensure Qdrant is running
docker ps | grep qdrant

# Restart Qdrant
docker run -p 6333:6333 qdrant/qdrant
```

### CORS Issues
- Ensure frontend is on `http://localhost:3000`
- Ensure backend is on `http://localhost:8000`
- Check CORS settings in `app/api.py`

### No Documents Available
```bash
# Run the indexing pipeline first
$env:PYTHONPATH = "."; python app/main.py
```

## 📚 Project Structure

```
rag-pipeline/
├── app/
│   ├── api.py                 # FastAPI server
│   ├── main.py               # Indexing pipeline
│   ├── rag.py                # RAG logic
│   ├── config.py             # Configuration
│   ├── embeddings/           # Embedding service
│   ├── llm/                  # LLM service
│   ├── vectorstore/          # Vector database
│   ├── chunking/             # Text chunking
│   ├── document_loader/      # PDF loading
│   ├── storage/              # Document store
│   └── models/               # Data models
├── chatbot/                  # Next.js frontend
│   ├── app/
│   │   ├── page.tsx         # Home page (redirects to chat)
│   │   ├── chat/
│   │   │   └── page.tsx     # Chat interface
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── ChatMessage.tsx  # Message display
│   │   ├── ChatInput.tsx    # Input field
│   │   └── Sidebar.tsx      # Document sidebar
│   └── .env.local           # Environment config
├── data/
│   └── documents/           # PDF documents
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Deployment

### Using Docker

Create `Dockerfile` for the backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Deploy Next.js:
```bash
cd chatbot
npm run build
npm start
```

## 📝 License

MIT License

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation at `/docs`
3. Check console logs for errors

---

**Happy chatting! 🎉**
