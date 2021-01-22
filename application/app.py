from flask import Flask, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, name):
        return {"data": name}

api.add_resource(HelloWorld, "/hello/<string:name>")

class PaymentMethod(Resource):
    def post(self):
        body = json.loads(request.body)
        return {"data":body}

api.add_resource(PaymentMethod,"/payment")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)