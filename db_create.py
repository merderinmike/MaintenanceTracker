from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

password = os.environ.get("MONGOPW")

cluster = MongoClient(
    f"""mongodb+srv://ashehorn:{password}@cluster0.4miwcyq.mongodb.net/?retryWrites=true&w=majority""")
db = cluster["Maintenance"]
collection = db["Vehicles"]

# post = {"_id": 0, "Vehicle": "Tacoma", "year": 2006}
# collection.insert_one(post)



