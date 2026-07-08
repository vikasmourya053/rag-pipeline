#!/usr/bin/env python3
"""Test Qdrant connection and configuration."""

from app.vectorstore.qdrant_store import QdrantStore
from app.config import QDRANT_URL, QDRANT_COLLECTION_NAME

print("=" * 60)
print("Testing Qdrant Connection")
print("=" * 60)

try:
    store = QdrantStore()
    
    # Test health
    if store.health_check():
        print(f"✅ Qdrant is healthy!")
        print(f"   URL: {QDRANT_URL}")
        print(f"   Collection: {QDRANT_COLLECTION_NAME}")
    else:
        print("❌ Qdrant connection failed")
        exit(1)
    
    # List collections
    collections = store.client.get_collections()
    print(f"\n📚 Available Collections: {len(collections.collections)}")
    for col in collections.collections:
        print(f"   - {col.name}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Ready to index documents.")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
