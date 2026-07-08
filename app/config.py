import os
from dotenv import load_dotenv

load_dotenv()

# ====== LLM Configuration ======
LLM_URL = os.getenv("LLM_URL", "http://57.159.31.11/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF")

# ====== Qdrant Configuration ======
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)  # For Qdrant Cloud
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "rag_documents")

# ====== Embedding Configuration ======
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384  # For all-MiniLM-L6-v2