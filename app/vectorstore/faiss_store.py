import faiss
import pickle
import numpy as np
import os


class FAISSStore:

    def __init__(self, dimension=None):
        self.dimension = dimension
        self.index = None
        self.chunks = []

        if dimension is not None:
            self.index = faiss.IndexFlatL2(dimension)

    def add(self, embeddings, chunks):
        embeddings = np.asarray(embeddings, dtype=np.float32)

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def save(self, folder="data/index"):

        os.makedirs(folder, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(folder, "index.faiss")
        )

        with open(
            os.path.join(folder, "chunks.pkl"),
            "wb"
        ) as f:
            pickle.dump(self.chunks, f)

    def load(self, folder="data/index"):

        self.index = faiss.read_index(
            os.path.join(folder, "index.faiss")
        )

        with open(
            os.path.join(folder, "chunks.pkl"),
            "rb"
        ) as f:
            self.chunks = pickle.load(f)

    def search(self, query_embedding, k=3):

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results