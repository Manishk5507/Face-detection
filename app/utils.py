from app.find_best_embedding import find_best_embedding
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGODB_URI')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['face_recognition_db']
collection = db['embeddings']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Function to save embeddings
def save_embedding_to_db(embedding, data):
    # If embedding is a NumPy array, convert it to a list
    if isinstance(embedding, np.ndarray):
        embedding = embedding.tolist()

    # Prepare the document to be inserted into the database
    document = {
        'embedding': embedding, # Save the embedding (list or array)
        'name': data['name'],
        'age': data['age'],
        'email': data['email'],
        'phone': data['phone'],
        'address': data['address'],
    }

    # Insert the document into the MongoDB collection
    collection.insert_one(document)

# Function to retrieve all embeddings from the database
def get_all_embeddings_from_db():
    return list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's default ID
