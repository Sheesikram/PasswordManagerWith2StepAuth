from collections import defaultdict
import math

class MovieRecommender:
    def __init__(self):
        # Sample movie ratings data
        self.ratings = {
            'Alice': {'Inception': 5, 'The Matrix': 4, 'Interstellar': 5, 'The Dark Knight': 4},
            'Bob': {'Inception': 3, 'The Matrix': 5, 'The Dark Knight': 5},
            'Charlie': {'Inception': 4, 'The Matrix': 4, 'Interstellar': 3, 'The Dark Knight': 2},
            'David': {'The Matrix': 3, 'Interstellar': 5, 'The Dark Knight': 4},
            'Eve': {'Inception': 5, 'Interstellar': 4, 'The Dark Knight': 5}
        }

    def calculate_similarity(self, user1, user2):
        """Calculate similarity between two users using cosine similarity"""
        common_movies = set(self.ratings[user1].keys()) & set(self.ratings[user2].keys())
        if not common_movies:
            return 0
        
        # Calculate dot product
        dot_product = sum(self.ratings[user1][movie] * self.ratings[user2][movie] for movie in common_movies)
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(self.ratings[user1][movie]**2 for movie in common_movies))
        magnitude2 = math.sqrt(sum(self.ratings[user2][movie]**2 for movie in common_movies))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)

    def get_recommendations(self, user):
        """Get movie recommendations for a user"""
        if user not in self.ratings:
            return []
        
        # Calculate similarities with other users
        similarities = {}
        for other_user in self.ratings:
            if other_user != user:
                similarities[other_user] = self.calculate_similarity(user, other_user)
        
        # Get movies the user hasn't watched
        user_movies = set(self.ratings[user].keys())
        all_movies = set()
        for user_ratings in self.ratings.values():
            all_movies.update(user_ratings.keys())
        unwatched_movies = all_movies - user_movies
        
        # Calculate predicted ratings
        predictions = {}
        for movie in unwatched_movies:
            weighted_sum = 0
            similarity_sum = 0
            
            for other_user in self.ratings:
                if other_user != user and movie in self.ratings[other_user]:
                    similarity = similarities[other_user]
                    weighted_sum += similarity * self.ratings[other_user][movie]
                    similarity_sum += abs(similarity)
            
            if similarity_sum > 0:
                predictions[movie] = weighted_sum / similarity_sum
        
        # Sort and return top recommendations
        return sorted(predictions.items(), key=lambda x: x[1], reverse=True)

    def print_recommendations(self, user):
        """Print recommendations for a user"""
        print(f"\nRecommendations for {user}:")
        print("Currently rated movies:")
        for movie, rating in self.ratings[user].items():
            print(f"- {movie}: {rating}")
        
        print("\nRecommended movies:")
        recommendations = self.get_recommendations(user)
        for movie, predicted_rating in recommendations:
            print(f"- {movie}: {predicted_rating:.2f}")

def main():
    recommender = MovieRecommender()
    test_users = ['Alice', 'Bob', 'David']
    
    print("Movie Recommendation System")
    print("==========================")
    
    for user in test_users:
        recommender.print_recommendations(user)

if __name__ == "__main__":
    main()