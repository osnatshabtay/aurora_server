import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pathlib import Path

def load_models():
    current_dir = Path(__file__).parent
    kmeans_model_path = current_dir / "kmeans_model.pkl"
    user_embeddings_path = current_dir / "user_embeddings.pkl"

    with open(kmeans_model_path, 'rb') as f:
        kmeans_model = pickle.load(f)

    with open(user_embeddings_path, 'rb') as f:
        user_embeddings = pickle.load(f)

    sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

    return kmeans_model, user_embeddings, sentence_transformer

def predict_cluster(embedding: np.ndarray, kmeans_model) -> int:
    embedding_2d = embedding.reshape(1, -1)  # הפיכה ל־2D
    return int(kmeans_model.predict(embedding_2d)[0])

def recommend_similar_users(new_embedding: np.ndarray, user_embeddings: dict, cluster_id: int, top_k: int = 5) -> list[str]:
    usernames = user_embeddings["usernames"]
    vectors = np.array(user_embeddings["vectors"], dtype=np.float32)
    clusters = user_embeddings["clusters"]

    same_cluster_indices = [i for i, c in enumerate(clusters) if c == cluster_id]
    if not same_cluster_indices:
        return []

    same_cluster_vectors = [vectors[i] for i in same_cluster_indices]
    same_cluster_usernames = [usernames[i] for i in same_cluster_indices]

    same_cluster_vectors = np.array(same_cluster_vectors, dtype=np.float32)  
    new_embedding_reshaped = new_embedding.reshape(1, -1).astype(np.float32)  
    similarities = cosine_similarity(new_embedding_reshaped, same_cluster_vectors)[0]
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    return [same_cluster_usernames[i] for i in top_k_indices]

async def update_user_recommendations_in_db(username: str, embedding: np.ndarray, cluster_id: int, recommended_usernames: list[str], users_collection) -> None:
    embedding_list = embedding.tolist()
    await users_collection.update_one(
        {"username": username},
        {
            "$set": {
                "embedding": embedding_list,
                "cluster_id": cluster_id,
                "recommended_users": recommended_usernames
            }
        }
    )

async def process_questionnaire_answers(answers: dict, username: str, users_collection) -> None:
    kmeans_model, user_embeddings, sentence_transformer = load_models()
    answers_list = answers.get("answers", [])
    if not answers_list:
        return
    combined_text = " ".join([str(answer) for answer in answers_list])

    embedding = sentence_transformer.encode(combined_text)
    embedding = np.array(embedding, dtype=np.float32)  

    cluster_id = predict_cluster(embedding, kmeans_model)
    recommended_usernames = recommend_similar_users(embedding, user_embeddings, cluster_id)
    await update_user_recommendations_in_db(username, embedding, cluster_id, recommended_usernames, users_collection)
