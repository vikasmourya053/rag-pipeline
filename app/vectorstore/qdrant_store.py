from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, EMBEDDING_DIMENSION


class QdrantStore:
    """Vector store using Qdrant for similarity search."""

    def __init__(self, collection_name=QDRANT_COLLECTION_NAME, url=QDRANT_URL, api_key=QDRANT_API_KEY):
        """
        Initialize Qdrant store.
        
        Args:
            collection_name: Name of the Qdrant collection
            url: Qdrant server URL (e.g., "http://localhost:6333")
            api_key: API key for Qdrant Cloud (optional)
        """
        self.collection_name = collection_name
        self.client = QdrantClient(url=url, api_key=api_key)
        self.chunks = {}  # Store chunks by point ID
        self.next_id = 0

    def create_collection(self, dimension=EMBEDDING_DIMENSION):
        """Create a new collection if it doesn't exist."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"✅ Collection '{self.collection_name}' already exists")
        except Exception:
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=dimension,
                    distance=Distance.COSINE
                ),
            )
            print(f"✅ Created collection '{self.collection_name}'")

    def add(self, embeddings, chunks):
        """
        Add embeddings and chunks to the store.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of chunk objects with text and metadata
        """
        points = []
        
        for embedding, chunk in zip(embeddings, chunks):
            point_id = self.next_id
            
            # Store chunk by ID
            self.chunks[point_id] = chunk
            
            # Create Qdrant point with metadata as payload
            point = PointStruct(
                id=point_id,
                vector=embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                payload={
                    "text": chunk.text,
                    "metadata": chunk.metadata
                }
            )
            points.append(point)
            self.next_id += 1
        
        # Upsert points to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        print(f"✅ Added {len(points)} points to Qdrant")

    def search(self, query_embedding, k=3):
        """
        Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of chunk objects
        """
        from app.models.chunk import Chunk
        
        query_vector = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding
        
        # Use query_points instead of search in this Qdrant client version
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=k,
            with_payload=True
        )
        
        chunks = []
        for result in results.points:
            # Reconstruct chunk from payload
            payload = result.payload
            if payload:
                chunk = Chunk(
                    text=payload.get("text", ""),
                    metadata=payload.get("metadata", {})
                )
                chunks.append(chunk)
        
        return chunks

    def delete(self, point_ids):
        """Delete points from collection."""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=point_ids
        )
        for point_id in point_ids:
            if point_id in self.chunks:
                del self.chunks[point_id]
        print(f"✅ Deleted {len(point_ids)} points")

    def clear(self):
        """Clear entire collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self.chunks = {}
            self.next_id = 0
            self.create_collection()
            print(f"✅ Cleared collection '{self.collection_name}'")
        except Exception as e:
            print(f"❌ Error clearing collection: {e}")

    def get_collection_info(self):
        """Get information about the collection."""
        collection_info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "points_count": collection_info.points_count
        }

    def health_check(self):
        """Check if Qdrant server is healthy."""
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False
