from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, name):
        return {"data": name}

api.add_resource(HelloWorld, "/hello/<string:name>")

#   check if required fields in request body of Payment method
paymentFields = reqparse.RequestParser()
paymentFields.add_argument("CreditCardNumber", type=str, help= "CreditCardNumber", required=True)
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder", required=True)
paymentFields.add_argument("ExpirationDate", type=str, help= "ExpirationDate", required=True)
paymentFields.add_argument("SecurityCode", type=str, help= "SecurityCode", required=True)
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder", required=True)
paymentFields.add_argument("Amount", type=float, help= "Amount", required=True)

class PaymentMethod(Resource):
    def post(self):
        args = paymentFields.parse_args() 
        return {"data":args}

api.add_resource(PaymentMethod,"/payment")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)