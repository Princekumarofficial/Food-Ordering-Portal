import logging
from abc import ABC, abstractmethod

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from business.models import FoodItem, Hotel
from rest_framework.response import Response
from business.serializers import FoodItemSerializer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodItemRecommendationMethod(ABC):
    """Abstract base class for food item recommendation methods."""

    @abstractmethod
    def recommend(self) -> Response:
        """Abstract method to be implemented for recommending food items."""
        pass


class RecommendByFoodItem(FoodItemRecommendationMethod):
    """
    Recommendation based on a specific food item.

    This class provides a method to recommend food items that are similar to a given food item ID.
    
    Attributes:
        fooditem_id (int): The ID of the food item for which recommendations are to be made.
    """

    """
        Initializes the RecommendByFoodItem with a specific food item ID.

        Args:
            fooditem_id (int): The ID of the food item for which recommendations are to be made.
    """

    """
        Recommend food items similar to the given food item ID.

        This method retrieves the food item corresponding to the provided food item ID, calculates
        the cosine similarity between the embedding of the given food item and other food items,
        and returns the top 5 most similar food items.

        Returns:
            Response: A Django REST framework Response object containing the recommended food items
                      or an error message if the food item is not found.
        
        Raises:
            FoodItem.DoesNotExist: If the food item with the given ID does not exist.
        """




    """Recommendation based on a specific food item."""

    def __init__(self, fooditem_id: int, hotel_id: int):
        self.fooditem_id = fooditem_id
        self.hotel_id = hotel_id

    def recommend(self, num: int = 5) -> Response:
        """Recommend food items similar to the given food item ID."""
        try:
            current_food_item = FoodItem.objects.get(pk=self.fooditem_id)
        except FoodItem.DoesNotExist:
            logger.error(f"FoodItem with id {self.fooditem_id} not found.")
            return Response({"error": "FoodItem not found"}, status=404)

        current_embedding = np.array(current_food_item.embedded_vector).reshape(1, -1)

        hotel = Hotel.objects.get(pk=self.hotel_id)
        other_food_items  = hotel.food_items.exclude(id=self.fooditem_id)
        similarities = []

        for food_item in other_food_items:
            food_item_embedding = np.array(food_item.embedded_vector).reshape(1, -1)
            similarity_score = cosine_similarity(current_embedding, food_item_embedding)[0][0]
            similarities.append((FoodItemSerializer(food_item).data, similarity_score))

        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:num]
        recommendations = [sim[0] for sim in similarities]
        return Response(recommendations, status=200)


class RecommendByText(FoodItemRecommendationMethod):
    """Recommendation based on text input."""

    EXTRA_STOP_WORDS = ["recipe", "recipes", "food"]

    def __init__(self, text: str):
        self.text = text

    def recommend(self, num) -> Response:
        """Recommend food items based on the given text."""
        

        # TODO: Recommend based on text inputs.


class FoodItemRecommender:
    """Facade for food item recommendation methods."""

    def fooditem_recommendations_by_id(self, pk: int, num: int = 5, hotel_id: int = 0) -> Response:
        """Get recommendations based on food item ID."""
        recommender = RecommendByFoodItem(pk, hotel_id)
        return recommender.recommend()

    def fooditem_recommendations_by_text(self, text: str, num: int = 5) -> Response:
        """Get recommendations based on text input."""
        recommender = RecommendByText(text)
        return recommender.recommend(num)
