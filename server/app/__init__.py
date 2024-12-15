from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/player/<string:player_id>")
def get_player(player_id):
   # Connect to MongoDB Atlas
    mongo_uri = os.getenv("MONGO_URI")
    print("got mongo uri{}".format(mongo_uri))
    client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    print("init client ")
    db = client["your_database_name"]
    collection = db["your_collection_name"]

    # Fetch player data from MongoDB
    print("attempting find one")
    player_data = collection.find_one({"player_id": player_id})

    if player_data:
        return f"<p>Player ID: {player_id}</p><p>Player Name: {player_data['name']}</p>"
    else:
        return "<p>Player not found</p>"