"""
Program: Collaborative Filtering Recommendation System using Matrix Factorization (SVD) from Scratch
Author: Lydia S. Makiwa
Date: June 7, 2026
Category: Machine Learning / Python Basics

Description:
This program implements a basic Collaborative Filtering recommender system using Matrix Factorization
via Stochastic Gradient Descent (SGD). It decomposes a sparse rating matrix into user and item 
latent factor matrices, enabling us to predict missing ratings and recommend new items to users.
"""
import numpy as np

class MatrixFactorizationSVD:
    def __init__(self, R, K, alpha=0.002, beta=0.02, steps=5000):
        """
        R: Rating matrix (user-item) where 0 indicates a missing rating
        K: Number of latent features
        alpha: Learning rate for SGD
        beta: Regularization parameter
        steps: Number of iterations
        """
        self.R = R
        self.num_users, self.num_items = R.shape
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.steps = steps

    def train(self):
        # Initialize user (P) and item (Q) latent feature matrices with random values
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

        # Find indices of non-zero (known) ratings
        self.samples = [
            (i, j, self.R[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.R[i, j] > 0
        ]

        # Perform Stochastic Gradient Descent
        for step in range(self.steps):
            np.random.shuffle(self.samples)
            for i, j, r in self.samples:
                # Predict rating
                prediction = self.get_rating(i, j)
                # Compute error
                error = r - prediction

                # Update user and item latent feature vectors
                p_i = self.P[i, :].copy()
                self.P[i, :] += self.alpha * (2 * error * self.Q[j, :] - self.beta * self.P[i, :])
                self.Q[j, :] += self.alpha * (2 * error * p_i - self.beta * self.Q[j, :])

            # Calculate mean squared error periodically
            if (step + 1) % 1000 == 0:
                mse = self.calculate_mse()
                print(f"Iteration {step + 1}/{self.steps} - Mean Squared Error (MSE): {mse:.4f}")

    def get_rating(self, i, j):
        """Get predicted rating for user i and item j"""
        return self.P[i, :].dot(self.Q[j, :].T)

    def calculate_mse(self):
        """Calculate MSE on non-zero ratings"""
        xs, ys = self.R.nonzero()
        predicted_R = self.full_matrix()
        error = 0
        for x, y in zip(xs, ys):
            error += (self.R[x, y] - predicted_R[x, y]) ** 2
        return error / len(xs)

    def full_matrix(self):
        """Get the fully reconstructed rating matrix"""
        return self.P.dot(self.Q.T)

# Demo / Working Example
if __name__ == "__main__":
    print("=== Matrix Factorization Recommendation System Demo ===")
    
    # 5 Users and 4 Items. 0 represents unrated item.
    # Rows: Users (Alice, Bob, Charlie, David, Eve)
    # Columns: Items (Movie1, Movie2, Movie3, Movie4)
    ratings = np.array([
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ])

    print("Original Ratings Matrix (0 = Unrated):")
    print(ratings)

    # Factorize with 2 latent features
    svd = MatrixFactorizationSVD(ratings, K=2, alpha=0.01, beta=0.02, steps=2000)
    print("\nTraining Matrix Factorization Model...")
    svd.train()

    reconstructed_matrix = svd.full_matrix()
    print("\nReconstructed Ratings Matrix (All ratings predicted):")
    print(np.round(reconstructed_matrix, 2))

    # Recommend for Alice (User 0)
    print("\nAlice\'s rating predictions:")
    for j in range(ratings.shape[1]):
        if ratings[0, j] == 0:
            print(f" -> Predicted rating for Movie {j+1} (originally unrated): {reconstructed_matrix[0, j]:.2f} \u2605")
        else:
            print(f" -> Actual rating for Movie {j+1}: {ratings[0, j]} \u2605 (Predicted: {reconstructed_matrix[0, j]:.2f} \u2605)")
