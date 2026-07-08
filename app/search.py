from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore

embedding_service = EmbeddingService()

store = QdrantStore()

question = input("Ask a question: ")

query_embedding = embedding_service.embed([question])[0]

results = store.search(query_embedding)

print("\nTop Results\n")

for chunk in results:
    print("=" * 60)
    print(chunk.metadata)
    print(chunk.text)