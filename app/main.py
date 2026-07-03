# # from pathlib import Path

# # from app.document_loader.pdf_loader import PDFLoader
# # from app.chunking.chunker import Chunker
# # from app.embeddings.embedding_service import EmbeddingService

# # documents = []

# # # Load all PDFs
# # for pdf_path in Path("data/documents").glob("*.pdf"):
# #     print(f"Loading: {pdf_path}")

# #     loader = PDFLoader(str(pdf_path))
# #     docs = loader.load()

# #     documents.extend(docs)

# # print(f"\nTotal Documents: {len(documents)}")

# # # Chunking
# # chunker = Chunker(chunk_size=300)
# # chunks = chunker.split(documents)

# # print(f"Total Chunks: {len(chunks)}")

# # # -------------------------
# # # Embeddings
# # # -------------------------

# # embedding_service = EmbeddingService()

# # # Extract text from each chunk
# # texts = [chunk.text for chunk in chunks]

# # # Convert text into vectors
# # embeddings = embedding_service.embed(texts)

# # print(f"Total Embeddings: {len(embeddings)}")
# # print(f"Embedding Dimension: {len(embeddings[0])}")

# # # Print first embedding (optional)
# # print("\nFirst Embedding:")
# # print(embeddings[0])







# from pathlib import Path

# from app.document_loader.pdf_loader import PDFLoader
# from app.chunking.chunker import Chunker
# from app.embeddings.embedding_service import EmbeddingService
# from app.vectorstore.faiss_store import FAISSStore

# documents = []

# # Load all PDFs
# for pdf_path in Path("data/documents").glob("*.pdf"):
#     print(f"Loading: {pdf_path}")

#     loader = PDFLoader(str(pdf_path))
#     docs = loader.load()

#     documents.extend(docs)

# print(f"\nTotal Documents: {len(documents)}")

# # -------------------------
# # Chunking
# # -------------------------
# chunker = Chunker(chunk_size=300)
# chunks = chunker.split(documents)

# print(f"Total Chunks: {len(chunks)}")

# # -------------------------
# # Embeddings
# # -------------------------
# embedding_service = EmbeddingService()

# texts = [chunk.text for chunk in chunks]

# embeddings = embedding_service.embed(texts)

# print(f"Total Embeddings: {len(embeddings)}")
# print(f"Embedding Dimension: {embeddings.shape[1]}")

# # -------------------------
# # FAISS
# # -------------------------
# dimension = embeddings.shape[1]

# store = FAISSStore(dimension)

# store.add(embeddings, chunks)

# store.save()

# print("Indexing Completed Successfully!")
































from pathlib import Path
import pickle

from app.document_loader.pdf_loader import PDFLoader
from app.chunking.chunker import Chunker
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.faiss_store import FAISSStore

documents = []

# -------------------------
# Load all PDFs
# -------------------------
for pdf_path in Path("data/documents").glob("*.pdf"):
    print(f"Loading: {pdf_path}")

    loader = PDFLoader(str(pdf_path))
    docs = loader.load()

    documents.extend(docs)

print(f"\nTotal Documents: {len(documents)}")

# -------------------------
# Chunking
# -------------------------
chunker = Chunker(chunk_size=300)
chunks = chunker.split(documents)

print(f"Total Chunks: {len(chunks)}")

# -------------------------
# Build Document Store
# -------------------------
document_store = {}

for chunk in chunks:
    file_name = chunk.metadata["file_name"]

    if file_name not in document_store:
        document_store[file_name] = []

    document_store[file_name].append(chunk)

print(f"Total Documents in Store: {len(document_store)}")

# Create storage folder
Path("storage").mkdir(exist_ok=True)

# Save document store
with open("storage/document_store.pkl", "wb") as f:
    pickle.dump(document_store, f)

print("✅ Document Store Saved.")

# -------------------------
# Embeddings
# -------------------------
embedding_service = EmbeddingService()

texts = [chunk.text for chunk in chunks]

embeddings = embedding_service.embed(texts)

print(f"Total Embeddings: {len(embeddings)}")
print(f"Embedding Dimension: {embeddings.shape[1]}")

# -------------------------
# FAISS
# -------------------------
dimension = embeddings.shape[1]

store = FAISSStore(dimension)

store.add(embeddings, chunks)

store.save()

print("✅ FAISS Index Saved.")
print("✅ Indexing Completed Successfully!")