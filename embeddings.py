from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import hashlib
from threading import Lock


class PDFVectorStore:
    """
    FAISS-based vector store with disk caching
    Safe for Flask multi-request usage
    """

    _lock = Lock()   # prevents race conditions

    def __init__(self, model_name="all-MiniLM-L6-v2", cache_dir="vector_cache"):
        self.model = SentenceTransformer(model_name)
        self.cache_dir = cache_dir
        self.index = None
        self.chunks = []
        self.index_loaded = False

        os.makedirs(cache_dir, exist_ok=True)

    def _hash_chunks(self, chunks):
        """
        Create a stable hash for PDF content
        """
        joined = "".join(chunks).encode("utf-8")
        return hashlib.md5(joined).hexdigest()

    def build_index(self, chunks):
        """
        Build or load FAISS index (only once)
        """
        if self.index_loaded:
            return

        with self._lock:
            if self.index_loaded:
                return

            self.chunks = chunks
            content_hash = self._hash_chunks(chunks)

            index_path = os.path.join(self.cache_dir, f"{content_hash}.index")
            chunks_path = os.path.join(self.cache_dir, f"{content_hash}.pkl")

            # ✅ Load cached index if available
            if os.path.exists(index_path) and os.path.exists(chunks_path):
                self.index = faiss.read_index(index_path)
                with open(chunks_path, "rb") as f:
                    self.chunks = pickle.load(f)

                self.index_loaded = True
                return

            # ❌ Build new index (only once)
            embeddings = self.model.encode(
                chunks,
                convert_to_numpy=True,
                show_progress_bar=True
            ).astype("float32")

            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(embeddings)

            # ✅ Save cache
            faiss.write_index(self.index, index_path)
            with open(chunks_path, "wb") as f:
                pickle.dump(chunks, f)

            self.index_loaded = True

    def search(self, query, top_k=3):
        """
        Search relevant PDF chunks
        """
        if not self.index_loaded:
            raise RuntimeError("Vector index not built")

        query_vec = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        _, indices = self.index.search(query_vec, top_k)

        return [self.chunks[i] for i in indices[0]]
