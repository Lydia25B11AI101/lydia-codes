"""
Program  : 53_recommendation_system.py
Title    : Movie Recommendation System (Collaborative Filtering)
Author   : Lydia S. Makiwa
Date     : 2026-06-01

Description:
    Builds a simple movie recommendation system using cosine similarity
    and collaborative filtering. Given a user's ratings of movies,
    finds similar movies and recommends the top ones.
    Perfect for understanding the fundamentals of recommendation
    engines used by Netflix, YouTube, and Spotify.
"""

import numpy as np
from collections import defaultdict


def create_user_movie_matrix(ratings, all_movies):
    """
    Convert user ratings into a matrix.
    ratings: dict of {user_id: {movie: rating}}
    all_movies: sorted list of all movie titles
    Returns a numpy array: users x movies
    """
    users = sorted(ratings.keys())
    matrix = np.zeros((len(users), len(all_movies)))
    movie_to_idx = {m: i for i, m in enumerate(all_movies)}
    
    for u_idx, user in enumerate(users):
        for movie, rating in ratings[user].items():
            if movie in movie_to_idx:
                matrix[u_idx, movie_to_idx[movie]] = rating
    
    return matrix, users


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors."""
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_similar_users(target_user, ratings, all_movies, k=3):
    """
    Find k most similar users to target_user.
    Uses cosine similarity on rating patterns.
    """
    matrix, users = create_user_movie_matrix(ratings, all_movies)
    target_idx = users.index(target_user)
    target_vector = matrix[target_idx]
    
    similarities = []
    for i, user in enumerate(users):
        if i == target_idx:
            continue
        sim = cosine_similarity(target_vector, matrix[i])
        similarities.append((sim, user))
    
    similarities.sort(reverse=True, key=lambda x: x[0])
    return similarities[:k]


def recommend_movies(target_user, ratings, all_movies, n_recommendations=5):
    """
    Recommend movies for target_user using collaborative filtering.
    Finds similar users and recommends movies they liked but
    the target user hasn't seen.
    """
    similar_users = find_similar_users(target_user, ratings, all_movies)
    
    # Get movies the target user has already rated
    watched = set(ratings.get(target_user, {}).keys())
    
    # Score unwatched movies based on similar users' ratings
    movie_scores = defaultdict(float)
    movie_counts = defaultdict(int)
    
    for sim_score, other_user in similar_users:
        for movie, rating in ratings[other_user].items():
            if movie not in watched:
                movie_scores[movie] += sim_score * rating
                movie_counts[movie] += 1
    
    # Average the scores
    avg_scores = {
        movie: movie_scores[movie] / max(movie_counts[movie], 1)
        for movie in movie_scores
    }
    
    recommendations = sorted(
        avg_scores.items(), key=lambda x: x[1], reverse=True
    )
    return recommendations[:n_recommendations]


# ===== DEMO =====
if __name__ == "__main__":
    # Sample movie ratings dataset
    all_movies = sorted([
        "The Matrix", "Inception", "Interstellar", "The Dark Knight",
        "Parasite", "Spirited Away", "Your Name", "Avengers: Endgame",
        "Toy Story", "Finding Nemo", "Up", "Coco"
    ])
    
    ratings = {
        "Alice": {
            "The Matrix": 5, "Inception": 5, "Interstellar": 4,
            "The Dark Knight": 5, "Parasite": 3, "Avengers: Endgame": 4,
            "Toy Story": 2
        },
        "Bob": {
            "The Matrix": 4, "Inception": 5, "Interstellar": 5,
            "The Dark Knight": 4, "Spirited Away": 2, "Your Name": 1
        },
        "Charlie": {
            "Parasite": 5, "Spirited Away": 5, "Your Name": 4,
            "Coco": 5, "Up": 4, "Finding Nemo": 3
        },
        "Diana": {
            "Inception": 3, "Interstellar": 5, "The Dark Knight": 4,
            "Parasite": 5, "Spirited Away": 4, "Your Name": 5,
            "Coco": 4, "Up": 3
        },
        "Eve": {
            "The Matrix": 5, "Inception": 4, "Interstellar": 5,
            "Avengers: Endgame": 5, "Toy Story": 4, "Finding Nemo": 4
        }
    }
    
    print("=" * 55)
    print("   MOVIE RECOMMENDATION SYSTEM — DEMO")
    print("=" * 55)
    
    target = "Alice"
    print(f"\nTarget user: {target}")
    print(f"Already watched: {', '.join(sorted(ratings[target].keys()))}")
    
    print("\nFinding similar users...")
    sim_users = find_similar_users(target, ratings, all_movies)
    for sim, user in sim_users:
        print(f"  → {user} (similarity: {sim:.3f})")
    
    print("\nTop recommendations for Alice:")
    recs = recommend_movies(target, ratings, all_movies, n_recommendations=5)
    for i, (movie, score) in enumerate(recs, 1):
        print(f"  {i}. {movie} — predicted rating: {score:.2f}")
    
    print("\n💡 Key insight: Collaborative filtering powers Netflix,")
    print("   Amazon, and Spotify recommendations!")
