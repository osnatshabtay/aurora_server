import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Load the model
model = SentenceTransformer("sentence-transformers/LaBSE")

# Path to the FAISS_data folder
base_path = os.path.join(os.path.dirname(__file__), "..", "FAISS_data")

# Load the FAISS binary file
faiss_index_path = os.path.join(base_path, "labse_index.faiss")
index = faiss.read_index(faiss_index_path)

# Load the texts and metadata
metadata_path = os.path.join(base_path, "labse_texts_metadata.pkl")
with open(metadata_path, "rb") as f:
    data = pickle.load(f)
    texts = data["texts"]
    metadata = data["metadata"]

# Semantic retrieval function
def search_similar_docs(query: str, top_k: int = 3):
    try:
        query_vec = model.encode(query, convert_to_numpy=True).astype("float32")
        D, I = index.search(np.array([query_vec]), top_k)
        return [texts[i] for i in I[0]]
    except Exception as e:
        print(f"🔴 שגיאה בשליפת מסמכים מהמאגר: {e}")
        return []
