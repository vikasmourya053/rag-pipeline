# from app.embeddings.embedding_service import EmbeddingService
# from app.vectorstore.faiss_store import FAISSStore
# from app.llm.llm_service import LLMService

# embedding_service = EmbeddingService()

# store = FAISSStore()
# store.load()

# llm = LLMService()

# while True:

#     question = input("\nAsk: ")

#     if question.lower() == "exit":
#         break

#     query_embedding = embedding_service.embed([question])[0]

#     chunks = store.search(query_embedding, k=3)

#     context = "\n\n".join(chunk.text for chunk in chunks)

#     answer = llm.generate(context, question)

#     print("\nAnswer:\n")
#     print(answer)










import pickle

from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.llm.llm_service import LLMService

# -------------------------
# Load Models
# -------------------------
embedding_service = EmbeddingService()

store = QdrantStore()
# Note: Collections are automatically loaded from Qdrant server
# No need to call load() like with FAISS

llm = LLMService()

# -------------------------
# Load Document Store
# -------------------------
with open("storage/document_store.pkl", "rb") as f:
    document_store = pickle.load(f)

print(f"Loaded {len(document_store)} documents.")

# -------------------------
# Chat Loop
# -------------------------
while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    # -------------------------
    # Check if a filename is mentioned
    # -------------------------
    matched_file = None

    for file_name in document_store.keys():
        if file_name.lower() in question.lower():
            matched_file = file_name
            break

    # ==================================================
    # Document Summary Mode
    # ==================================================
    if matched_file:

        print(f"\n📄 Document Found: {matched_file}")

        chunks = document_store[matched_file]

        context = "\n\n".join(chunk.text for chunk in chunks)

        answer = llm.generate(context, question)

    # ==================================================
    # Normal RAG Search
    # ==================================================
    else:

        query_embedding = embedding_service.embed([question])[0]

        chunks = store.search(query_embedding, k=3)

        context = "\n\n".join(chunk.text for chunk in chunks)

        answer = llm.generate(context, question)

    print("\nAnswer:\n")
    print(answer)