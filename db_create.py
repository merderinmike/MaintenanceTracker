from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from pymongo.collection import Collection
import os
import pandas as pd

load_dotenv(find_dotenv())

password = os.environ.get("MONGOPW")

cluster = MongoClient(
    f"""mongodb+srv://ashehorn:{password}@cluster0.4miwcyq.mongodb.net/?retryWrites=true&w=majority""")
db = cluster["Maintenance"]
vehicles = db["Vehicles"]
records = db['Records']
findVehicle = list(vehicles.find())
findRecord = list(records.find())
selection = []
recordModel = []
record = []
#db.Records.insert_one({"model":"tacoma", "miles": 230000,"date":"2023/24/1" ,"tasks":"oil change"})
for item in findVehicle:
    selection.append(f"{item['model']}")

for entry in findRecord:
    recordModel.append(f"{entry['model']}")
    record.append(f"{entry['model']}")
    record.append(f"{entry['miles']}")
    record.append(f"{entry['date']}")
    record.append(f"{entry['tasks']}")
#df = pd.DataFrame([record])
