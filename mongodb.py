import ast

import environs
import pandas as pd
import pymongo


class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient(environs.env.str("MONGODB_URI"))
        self.db = self.client["GuitarHero"]
        self.product_collection = self.db["products"]
        self.category_collection = self.db["categories"]

    def insert_product_data(self, data: pd.DataFrame):
        if not data.empty:
            self.product_collection.insert_many(data.to_dict(orient="records"))

    def insert_category_data(self, data):
        self.category_collection.insert_one(data)

    def get_categories(self):
        return self.category_collection.find()

    def get_category_by_name(self, name: str):
        return self.category_collection.find_one({"name": f"{name}"})


if __name__ == "__main__":
    mongo = MongoDB()

    df = pd.read_csv("shop_data/1__2 Size Classical Guitars.csv")

    category = mongo.get_category_by_name("1/2 Size Classical Guitars")

    if category:
        category_id = category["_id"]  # Extract the _id field
        df = df.rename(columns={"features": "parameters"})

        df["category"] = category_id

        df["images"] = df["images"].apply(ast.literal_eval)
        df["parameters"] = df["parameters"].apply(ast.literal_eval)

        mongo.insert_product_data(df)

    else:
        print("Document not found")
