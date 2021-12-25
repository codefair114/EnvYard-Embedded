from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    "")
db = client.get_database('Database')
records = db.parameters
im_records = db.images
plants_list = ["all", "tomatoes", "cucumber"]
media_type = ["text", "image", "video"]