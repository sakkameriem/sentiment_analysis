import pymongo
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["comments_Zitouna"]

def clean_text(text):
    text = re.sub(r"\\[uU][a-fA-F0-9]+", '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

cleaned_collection = db["cleaned_comments_Zitouna1"]


documents_to_update = collection.find({"text": {"$exists": True, "$ne": ""}})

for document in documents_to_update:
    cleaned_text = clean_text(document["text"])
    new_document = {
        "_id": document["_id"],
        "facebookUrl": document["facebookUrl"],
        "postTitle": document["postTitle"],
        "profileName": document["profileName"],
        "text": cleaned_text,
        "date": document["date"],
        "likesCount": document["likesCount"]
    }
    cleaned_collection.insert_one(new_document)

