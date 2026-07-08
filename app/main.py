from pathlib import Path

from app.document_loader.pdf_loader import PDFLoader
from app.chunking.chunker import Chunker
from app.embeddings.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.storage.document_store import DocumentStore

print("=" * 60)
print("RAG Pipeline - Document Indexing with Qdrant")
print("=" * 60)

# ====== Check Qdrant Connection ======
store = QdrantStore()
if not store.health_check():
    print("❌ ERROR: Qdrant server not running!")
    print("   Start Qdrant: docker run -p 6333:6333 qdrant/qdrant")
    exit(1)

print("✅ Connected to Qdrant")

# ====== Load PDFs ======
print("\n[1/5] Loading PDF documents...")
documents = []

pdf_path = Path("data/documents")
if not pdf_path.exists():
    print(f"⚠️  No documents found in {pdf_path}")
else:
    for pdf_file in pdf_path.glob("*.pdf"):
        print(f"  📄 Loading: {pdf_file.name}")
        loader = PDFLoader(str(pdf_file))
        docs = loader.load()
        documents.extend(docs)

print(f"✅ Loaded {len(documents)} pages from PDF(s)")

# ====== Chunking ======
print("\n[2/5] Chunking documents...")
chunker = Chunker(chunk_size=300)
chunks = chunker.split(documents)
print(f"✅ Created {len(chunks)} chunks")

# ====== Generate Embeddings ======
print("\n[3/5] Generating embeddings...")
embedding_service = EmbeddingService()
texts = [chunk.text for chunk in chunks]
embeddings = embedding_service.embed(texts)
print(f"✅ Generated {len(embeddings)} embeddings (dimension: {len(embeddings[0])})")

# ====== Store in Qdrant ======
print("\n[4/5] Storing embeddings in Qdrant...")
store.create_collection()
store.add(embeddings, chunks)
collection_info = store.get_collection_info()
print(f"✅ Collection Info: {collection_info}")

# ====== Save Document Store ======
print("\n[5/5] Saving document store...")
doc_store = DocumentStore()
for chunk in chunks:
    doc_store.add_chunk(chunk)
doc_store.save()

print("\n" + "=" * 60)
print("✅ Pipeline Complete! Ready for RAG queries.")
print("=" * 60)


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