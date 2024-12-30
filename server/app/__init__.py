from flask import Flask, request
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.json_util import dumps
import os
import certifi

# Load environment variables from .env file
load_dotenv()

def get_mongo_collection(collection_name):
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    db = client["nba"]
    collection = db[collection_name]
    return collection

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/player/<string:player_id>")
def get_player(player_id):

    collection = get_mongo_collection("players")

    # Fetch player data from MongoDB
    player_data = collection.find_one({"player_id": player_id})

    if player_data:
        return f"<p>Player ID: {player_id}</p><p>Player Name: {player_data['name']}</p>"
    else:
        return "<p>Player not found</p>"

@app.route("/gamelog/<string:player_id>")
def get_gamelog(player_id):
    collection = get_mongo_collection("gamelogs")
    
    # Get args
    num_gamelogs = int(request.args.get("num", 5))
    stat_names = request.args.get("stats")
    stat_query = {"_id": 1, "date_game": 1}

    for stat in stat_names.split(","):
        stat_query[stat] = 1
    
    # Log args
    app.logger.info(f"get_gamelog request -- num_gamelogs: {num_gamelogs}, stat_names: {stat_names}")
    
    # Fetch gamelog data from MongoDB
    gamelogs = collection.find(
        { "_id.player_id": player_id },
        stat_query
    ).sort({ "date_game": -1 }).limit(num_gamelogs)
    
    if gamelogs:
        return dumps(list(gamelogs))
    else:
        return "<p>Gamelogs not found</p>"