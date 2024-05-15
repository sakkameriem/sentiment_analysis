import pymongo
import pandas as pd
import re
from IPython.display import display

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["comments_Zitouna"]

def clean_text(text):
    # remove special characters ( Arabic & French )
    cleaned_text = re.sub(r'[^\w\sàâçéèêëîïôûùüÿæœÀÂÇÉÈÊËÎÏÔÛÙÜŸÆŒéàèùêûîôç]', ' ', text)
    # remove extra space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip().lower()
    return cleaned_text


Zitouna_df = pd.DataFrame(list(collection.find()))

# drop missing values and duplicates
cleaned_df = Zitouna_df.dropna(subset=['text'])
cleaned_df = cleaned_df.drop_duplicates(subset=['text'], keep='first')


collection_cleaned = db["cleaned_comments_Zitouna"]
collection_cleaned.insert_many(cleaned_df.to_dict(orient='records'))


for index, row in cleaned_df.iterrows():
    collection_cleaned.delete_many({'text': {'$eq': ''}})
    cleaned_text = clean_text(row['text'])
    collection_cleaned.update_one({'_id': row['_id']}, {'$set': {'text': cleaned_text}})
