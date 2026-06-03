# ==============================================================================
# Title: Simple Collaborative Filtering Recommendation System
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Implements a user-based collaborative filtering recommendation 
#              system from scratch. Uses Pearson Correlation Coefficient to 
#              find similar users and predicts ratings for unrated items.
#              Designed for first-year AIML students to understand recommendation mechanics.
# ==============================================================================

import math

def pearson_correlation(user1_ratings, user2_ratings):
    """
    Calculate the Pearson Correlation Coefficient between two users.
    Only considers items that BOTH users have rated.
    Returns a score between -1.0 and 1.0. Returns 0.0 if there's no correlation.
    """
    # Find items rated by both users
    common_items = [item for item in user1_ratings if item in user2_ratings]
    n = len(common_items)
    
    # If no common items, return 0
    if n == 0:
        return 0.0
    
    # Compute sums of ratings
    sum1 = sum(user1_ratings[item] for item in common_items)
    sum2 = sum(user2_ratings[item] for item in common_items)
    
    # Compute sum of squares of ratings
    sum1_sq = sum(user1_ratings[item] ** 2 for item in common_items)
    sum2_sq = sum(user2_ratings[item] ** 2 for item in common_items)
    
    # Compute sum of products of ratings
    p_sum = sum(user1_ratings[item] * user2_ratings[item] for item in common_items)
    
    # Calculate Pearson score
    num = p_sum - (sum1 * sum2 / n)
    den = math.sqrt((sum1_sq - (sum1 ** 2) / n) * (sum2_sq - (sum2 ** 2) / n))
    
    if den == 0:
        return 0.0
    
    return num / den

def get_recommendations(dataset, target_user):
    """
    Generate movie recommendations for a target user.
    Uses a weighted average of other users' ratings, weighted by their similarity score.
    """
    totals = {}
    similarity_sums = {}
    
    for other_user in dataset:
        # Don't compare a user to themselves
        if other_user == target_user:
            continue
            
        sim = pearson_correlation(dataset[target_user], dataset[other_user])
        
        # Ignore users with zero or negative correlation
        if sim <= 0:
            continue
            
        for item in dataset[other_user]:
            # Recommend only items the target user hasn't seen/rated yet
            if item not in dataset[target_user] or dataset[target_user][item] == 0:
                # Similarity * Rating
                totals.setdefault(item, 0)
                totals[item] += dataset[other_user][item] * sim
                
                # Sum of similarities
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += sim
                
    # Create the normalized list of recommendations
    rankings = []
    for item, total in totals.items():
        predicted_rating = total / similarity_sums[item]
        rankings.append((round(predicted_rating, 2), item))
        
    # Sort rankings in descending order
    rankings.sort(reverse=True)
    return rankings

# --- Demo & Example ---
if __name__ == "__main__":
    print("--- User-Based Collaborative Filtering Recommender Demo ---")
    
    # Dataset representing movie ratings (1 to 5 stars) from different users
    movie_ratings = {
        'Alice': {'Inception': 5, 'Interstellar': 4, 'The Matrix': 5, 'Toy Story': 1, 'Up': 2},
        'Bob': {'Inception': 5, 'Interstellar': 5, 'The Matrix': 4, 'Toy Story': 2, 'Up': 1},
        'Charlie': {'Inception': 2, 'Toy Story': 5, 'Up': 4, 'The Matrix': 2},
        'David': {'Interstellar': 4, 'The Matrix': 4, 'Toy Story': 2},
        'Eve': {'Inception': 1, 'Interstellar': 2, 'Toy Story': 5, 'Up': 5},
        'Lydia (Target)': {'Inception': 4, 'The Matrix': 5, 'Toy Story': 1} # Hasn't watched Interstellar or Up
    }
    
    print("\nDataset ratings for current users:")
    for user, ratings in movie_ratings.items():
        print(f"  {user}: {ratings}")
        
    print("\nCalculating Pearson Similarity between Lydia and other users:")
    for other in movie_ratings:
        if other != 'Lydia (Target)':
            sim = pearson_correlation(movie_ratings['Lydia (Target)'], movie_ratings[other])
            print(f"  Lydia <-> {other}: Similarity = {sim:.4f}")
            
    print("\nGenerating recommendations for Lydia:")
    recommendations = get_recommendations(movie_ratings, 'Lydia (Target)')
    
    if recommendations:
        for rating, movie in recommendations:
            print(f"  Recommended Movie: '{movie}' | Predicted Rating: {rating} stars")
    else:
        print("  No recommendations available.")
