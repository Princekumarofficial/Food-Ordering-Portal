import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from business.models import FoodItem, Hotel
from django.core.management.base import BaseCommand
import logging
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Command(BaseCommand):
    help = "Update the FoodItem model with new data from the CSV files"

    def handle(self, *args, **options):

        FoodItem.objects.all().delete()
        Hotel.objects.all().delete()

        path = os.path.join(os.getcwd(), 'data')
        csv_files = os.listdir(path)
        logging.info(f"csv_files loaded: {csv_files}")

        csv_file_paths = [os.path.join(path, file) for file in csv_files]
        recipies_csv = csv_file_paths[0]
        restaurants_csv = csv_file_paths[1]

        # Load the CSV and sample 500 rows
        recipies_df = pd.read_csv(recipies_csv)
        restaurants_df = pd.read_csv(restaurants_csv)
        recipies_df.dropna(inplace=True)
        restaurants_df.dropna(inplace=True)
        restaurants_df = restaurants_df.sample(n=20).reset_index(drop=True)
        recipies_df = recipies_df.sample(n=500).reset_index(drop=True)

        recipies_df["meta"] = recipies_df["TranslatedRecipeName"] + " " + recipies_df["Cuisine"] + " " + recipies_df["Cleaned-Ingredients"]
        recipies_df["meta"] = recipies_df["meta"].apply(lambda x: ' '.join(x.split()[:20]))

        # TF-IDF vectorizer
        tfidf = TfidfVectorizer(stop_words="english")
        extra_stop_words = ["recipe", "recipes", "food"]
        tfidf.stop_words = list(tfidf.get_stop_words()) + extra_stop_words
        tfidf_matrix = tfidf.fit_transform(recipies_df.meta.values.astype("U"))

        # Loop over DataFrame and create FoodItem objects
        for index, row in recipies_df.iterrows():
            # Get the embedding for this row and convert it to a list
            embedding_vector = tfidf_matrix[index].toarray().tolist()

            # Create FoodItem object
            try:
                food_item = FoodItem.objects.create(
                    name=row["TranslatedRecipeName"],
                    price=np.random.randint(100, 500),  # Example random price, adjust according to your data
                    veg=np.random.randint(0,2), 
                    nonVeg=np.random.randint(0,2), 
                    image=row["image-url"],
                    image_url=row["image-url"],
                    embedded_vector=embedding_vector
                )

                logging.info(f"Created FoodItem: {food_item.name}")
            
            except Exception as e:
                logging.error(e)

        for index, row in restaurants_df.iterrows():
            restaurant = Hotel.objects.create(
                name=row["restaurant name"],
                address=row["local address"] + " , " + row["area"],
                minPrice=row["avg cost (two people)"],
                rating=row["rate (out of 5)"], 
                veg=np.random.randint(0,2), 
                nonVeg=np.random.randint(0,2)
            )

            logging.info(f"Created Hotel: {restaurant.name}")

            random_number_of_food_items = np.random.randint(30, 80)
            
            food_items = FoodItem.objects.order_by('?')[:random_number_of_food_items]
            restaurant.image_url = food_items[0].image_url
            for food_item in food_items:
                restaurant.food_items.add(food_item)

            restaurant.save()
            logging.info(f"Added {random_number_of_food_items} food items to {restaurant.name}")

        logging.info("Data update complete")
