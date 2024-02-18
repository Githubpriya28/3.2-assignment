from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["football_team"]
players_collection = db["players"]

class PlayerResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("position", type=str, required=True)
        parser.add_argument("rushingYards", type=int)
        parser.add_argument("touchdownsThrown", type=int)
        parser.add_argument("sacks", type=int)
        parser.add_argument("fieldGoalsMade", type=int)
        parser.add_argument("fieldGoalsMissed", type=int)
        parser.add_argument("catchesMade", type=int)
        player_data = parser.parse_args()
        players_collection.insert_one(player_data)
        return {"message": "Player added successfully"}, 201

    def put(self, player_name):
        parser = reqparse.RequestParser()
        parser.add_argument("position", type=str)
        parser.add_argument("rushingYards", type=int)
        parser.add_argument("touchdownsThrown", type=int)
        parser.add_argument("sacks", type=int)
        parser.add_argument("fieldGoalsMade", type=int)
        parser.add_argument("fieldGoalsMissed", type=int)
        parser.add_argument("catchesMade", type=int)
        new_data = parser.parse_args()
        query = {"name": player_name}
        players_collection.update_one(query, {"$set": new_data})
        return {"message": "Player updated successfully"}, 200

    def delete(self, player_name):
        query = {"name": player_name}
        players_collection.delete_one(query)
        return {"message": "Player deleted successfully"}, 200

class QueryResource(Resource):
    def post(self):
        query = request.json
        result = players_collection.find(query)
        return dumps(result), 200

api.add_resource(PlayerResource, '/players')
api.add_resource(PlayerResource, '/players/<string:player_name>')
api.add_resource(QueryResource, '/players/query')

if __name__ == '__main__':
    app.run(debug=True)
