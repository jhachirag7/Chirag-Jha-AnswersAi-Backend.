from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()
key=os.environ.get('mongodb_pass')
appName=os.environ.get('appName')
uri = f"mongodb+srv://jhachirag7:{key}@cluster0.rnfwq8t.mongodb.net/?retryWrites=true&w=majority&appName={appName}"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db=client.answerai_db
collection=db['answerai_data']
collection_user=db['answerai_user']
# collection_likes=db['blog_like']