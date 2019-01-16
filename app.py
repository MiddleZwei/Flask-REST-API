from flask import Flask
from flask_restful import Api, Resource, reqparse
import os

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Jade",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Josh",
        "age": 21,
        "occupation": "Sales Manager"
    },
    {
        "name": "Agata",
        "age": 25,
        "occupation": "CEO"
    }
]


class User(Resource):
    def get(self, name):
        for user in users:
            if(name==user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name is already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupationb"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user)
        return user, 201


    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted".format(name), 200



api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
