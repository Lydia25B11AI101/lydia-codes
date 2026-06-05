# Program Title: Content-Based Movie Recommendation System from Scratch
# Author: Lydia S. Makiwa
# Date: June 5, 2026
# Description: Implements a content-based recommendation engine without advanced libraries.
#              It calculates Jaccard similarity between movie genre profiles and user preference
#              profiles to suggest highly personalized movies. Shows clean dictionary and set mapping.
#              Perfect for AIML students exploring collaborative/content filtering principles.

def calculate_jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0

class ContentBasedRecommender:
    def __init__(self, movie_database):
        self.movie_database = movie_database # Dict mapping Title to Set of Genres

    def recommend(self, user_liked_genres, num_recommendations=2):
        scores = []
        user_genre_set = set(user_liked_genres)
        
        for movie_title, genres in self.movie_database.items():
            similarity = calculate_jaccard_similarity(user_genre_set, genres)
            scores.append((movie_title, similarity, genres))
            
        # Sort by similarity score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:num_recommendations]

if __name__ == "__main__":
    # Movie dataset with genre sets
    movies = {
        "The Matrix": {"Sci-Fi", "Action", "Thriller"},
        "Inception": {"Sci-Fi", "Action", "Adventure", "Heist"},
        "Interstellar": {"Sci-Fi", "Adventure", "Drama"},
        "The Dark Knight": {"Action", "Crime", "Drama", "Thriller"},
        "Pulp Fiction": {"Crime", "Drama", "Thriller"},
        "Superbad": {"Comedy", "Romance"},
        "Toy Story": {"Animation", "Adventure", "Family", "Comedy"},
        "Spirited Away": {"Animation", "Fantasy", "Adventure"}
    }
    
    print("=== Content-Based Movie Recommender ===")
    recommender = ContentBasedRecommender(movies)
    
    # Simulating user preferences
    user_preferences = ["Sci-Fi", "Adventure"]
    print(f"\nUser Preference Genres: {user_preferences}")
    
    recommendations = recommender.recommend(user_preferences, num_recommendations=3)
    
    print("\n--- Top Recommendations ---")
    for idx, (movie, score, genres) in enumerate(recommendations, 1):
        print(f"{idx}. {movie} (Similarity: {score:.2%})")
        print(f"   Genres: {', '.join(genres)}")
