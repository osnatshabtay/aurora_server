import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pathlib import Path

def load_models():
    """Loads the KMeans model and user embeddings from disk."""
    # Get the current directory (where this file is located)
    current_dir = Path(__file__).parent
    
    # Define paths to model files
    kmeans_model_path = current_dir / "kmeans_model.pkl"
    user_embeddings_path = current_dir / "user_embeddings.pkl"
    
    # Load the KMeans model
    with open(kmeans_model_path, 'rb') as f:
        kmeans_model = pickle.load(f)
    
    # Load the user embeddings
    with open(user_embeddings_path, 'rb') as f:
        user_embeddings = pickle.load(f)
    
    # Initialize the sentence transformer model
    sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
    
    return kmeans_model, user_embeddings, sentence_transformer

def predict_cluster(embedding: np.ndarray, kmeans_model) -> int:
    """Predicts which cluster the new user belongs to using the KMeans model."""
    return int(kmeans_model.predict(embedding)[0])

def recommend_similar_users(
    new_embedding: np.ndarray,
    user_embeddings: dict,
    cluster_id: int,
    top_k: int = 5
) -> list[str]:
    """
    Finds the top-k most similar users to the new user from the same cluster.

    Arguments:
    - new_embedding: the vector of the new user (shape: 1 x embedding_dim)
    - user_embeddings: a dictionary containing:
        {
            "usernames": [list of usernames],
            "vectors": [list of np.ndarray embeddings],
            "clusters": [list of int cluster_ids for each user]
        }
    - cluster_id: the cluster ID assigned to the new user
    - top_k: how many recommended users to return (default: 5)

    Returns:
    - A list of usernames (strings) of the top-k most similar users from the same cluster.
    """
    # Extract usernames, vectors, and clusters from the user_embeddings dictionary
    usernames = user_embeddings["usernames"]
    vectors = user_embeddings["vectors"]
    clusters = user_embeddings["clusters"]
    
    # Find indices of users in the same cluster
    same_cluster_indices = [i for i, c in enumerate(clusters) if c == cluster_id]
    
    # If no users in the same cluster, return an empty list
    if not same_cluster_indices:
        return []
    
    # Extract vectors of users in the same cluster
    same_cluster_vectors = [vectors[i] for i in same_cluster_indices]
    same_cluster_usernames = [usernames[i] for i in same_cluster_indices]
    
    # Convert to numpy arrays for easier computation
    same_cluster_vectors = np.array(same_cluster_vectors)
    
    # Reshape new_embedding to match the expected format for cosine_similarity
    new_embedding_reshaped = new_embedding.reshape(1, -1)
    
    # Calculate cosine similarity between the new user and all users in the same cluster
    similarities = cosine_similarity(new_embedding_reshaped, same_cluster_vectors)[0]
    
    # Get indices of top-k most similar users
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Return usernames of the top-k most similar users
    return [same_cluster_usernames[i] for i in top_k_indices]

def update_user_recommendations_in_db(
    username: str,
    embedding: np.ndarray,
    cluster_id: int,
    recommended_usernames: list[str],
    users_collection
) -> None:
    """
    Updates the user document in MongoDB to include cluster and recommended users.

    Arguments:
    - username: the user to update
    - embedding: their vector (1D NumPy array)
    - cluster_id: predicted cluster
    - recommended_usernames: list of usernames from same cluster
    - users_collection: the MongoDB collection
    """
    # Convert the embedding to a list for MongoDB storage
    embedding_list = embedding.tolist()
    
    # Update the user document with the embedding, cluster ID, and recommended users
    users_collection.update_one(
        {"username": username},
        {
            "$set": {
                "embedding": embedding_list,
                "cluster_id": cluster_id,
                "recommended_users": recommended_usernames
            }
        }
    )

def process_questionnaire_answers(answers: dict, username: str, users_collection) -> None:
    """
    Process questionnaire answers to generate user embeddings and recommendations.
    
    Arguments:
    - answers: dictionary containing the user's answers to the questionnaire
    - username: the username of the user
    - users_collection: the MongoDB collection for users
    """
    # Load the models
    kmeans_model, user_embeddings, sentence_transformer = load_models()
    
    # Extract the answers from the dictionary
    answers_list = answers.get("answers", [])
    
    # If there are no answers, return early
    if not answers_list:
        return
    
    # Combine all answers into a single text for embedding
    combined_text = " ".join([str(answer) for answer in answers_list])
    
    # Generate embedding for the combined text
    embedding = sentence_transformer.encode(combined_text)
    
    # Predict the cluster for the user
    cluster_id = predict_cluster(embedding, kmeans_model)
    
    # Get recommended users from the same cluster
    recommended_usernames = recommend_similar_users(embedding, user_embeddings, cluster_id)
    
    # Update the user document in the database
    update_user_recommendations_in_db(username, embedding, cluster_id, recommended_usernames, users_collection) 