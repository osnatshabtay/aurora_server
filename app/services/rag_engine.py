import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# טען את המודל
model = SentenceTransformer("sentence-transformers/LaBSE")

# נתיב לתיקיית FAISS_data
base_path = os.path.join(os.path.dirname(__file__), "..", "FAISS_data")

# טען את הקובץ הבינארי של FAISS
faiss_index_path = os.path.join(base_path, "labse_index.faiss")
index = faiss.read_index(faiss_index_path)

# טען את הטקסטים והמטאדאטה
metadata_path = os.path.join(base_path, "labse_texts_metadata.pkl")
with open(metadata_path, "rb") as f:
    data = pickle.load(f)
    texts = data["texts"]
    metadata = data["metadata"]

# פונקציה לשליפה סמנטית
def search_similar_docs(query: str, top_k: int = 3):
    try:
        query_vec = model.encode(query, convert_to_numpy=True).astype("float32")
        D, I = index.search(np.array([query_vec]), top_k)
        return [texts[i] for i in I[0]]
    except Exception as e:
        print(f"🔴 שגיאה בשליפת מסמכים מהמאגר: {e}")
        return []
