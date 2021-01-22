from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, name):
        return {"data": name}

api.add_resource(HelloWorld, "/hello/<string:name>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)