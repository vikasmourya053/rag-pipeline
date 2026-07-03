from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.faiss_store import FAISSStore
from app.llm.llm_service import LLMService

embedding_service = EmbeddingService()

store = FAISSStore()
store.load()

llm = LLMService()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    query_embedding = embedding_service.embed([question])[0]

    chunks = store.search(query_embedding, k=3)

    context = "\n\n".join(chunk.text for chunk in chunks)

    answer = llm.generate(context, question)

    print("\nAnswer:\n")
    print(answer)