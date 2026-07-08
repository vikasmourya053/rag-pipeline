import pickle
from pathlib import Path


class DocumentStore:

    def __init__(self):
        self.documents = {}

    def add_chunk(self, chunk):
        file_name = chunk.metadata["file_name"]

        if file_name not in self.documents:
            self.documents[file_name] = []

        self.documents[file_name].append(chunk)

    def save(self, path="storage/document_store.pkl"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as f:
            pickle.dump(self.documents, f)

        print(f"✅ Document Store saved to {path}")

    def load(self, path="storage/document_store.pkl"):
        with open(path, "rb") as f:
            self.documents = pickle.load(f)

        print(f"✅ Loaded {len(self.documents)} documents.")

    def get_document(self, file_name):
        return self.documents.get(file_name)

    def get_all_documents(self):
        return self.documents

    def list_documents(self):
        return list(self.documents.keys())