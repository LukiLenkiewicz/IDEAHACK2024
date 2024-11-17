import numpy as np
import faiss
import os


class VectorStoreHandler:
    def __init__(self, vector_store_file="vector_store.index"):
        # Initialize FAISS for local vector store
        self.vector_dim = 384  # Dimension of the Sentence-BERT embeddings
        self.vector_store_file = vector_store_file

        # Load vector store
        self.load_vector_store()

    def load_vector_store(self):
        if os.path.exists(self.vector_store_file):
            # Load FAISS index
            self.index = faiss.read_index(self.vector_store_file)
            print("Vector store loaded successfully.")
        else:
            # Create a new FAISS index if none exists
            self.index = faiss.IndexFlatL2(self.vector_dim)
            print("No existing vector store found. A new one has been created.")

    def add_vector(self, embedding):
        # Add vector to FAISS index
        vector = np.array([embedding], dtype="float32")
        self.index.add(vector)
        vector_id = self.index.ntotal - 1  # The ID of the newly added vector
        # Save updated vector store
        faiss.write_index(self.index, self.vector_store_file)
        return vector_id

    def search_vectors(self, query_embedding, filtered_indices, top_k=5):
        # Create a temporary FAISS index for filtered vectors
        if not filtered_indices:
            print("No vectors to search in.")
            return []

        filtered_embeddings = [self.index.reconstruct(idx) for idx in filtered_indices]
        filtered_index = faiss.IndexFlatL2(self.vector_dim)
        filtered_index.add(np.array(filtered_embeddings, dtype="float32"))

        # Perform FAISS search on filtered index
        query_embedding = np.array([query_embedding], dtype="float32")
        distances, indices = filtered_index.search(query_embedding, top_k)
        results = []
        ids = []
        for i, dist in zip(indices[0], distances[0]):
            original_idx = filtered_indices[i]
            if original_idx not in ids:
                results.append({"id": original_idx, "score": dist})
                ids.append(original_idx)

        return results
