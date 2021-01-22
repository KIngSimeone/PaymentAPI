from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy



# Initialize flask app
app = Flask(__name__)

# Link to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Set app as API
api = Api(app)

# Set db as app datatbase
db = SQLAlchemy(app)


# Transaction record model
class TransactionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditCardNumber =  db.Column(db.String(100), unique = True, nullable=False)
    cardHolder =  db.Column(db.String(564),nullable=False)
    expiryDate = db.Column(db.Date,nullable=False)
    securityCode = db.Column(db.String(20),nullable=False)
    amount = db.Column(db.Float, nullable=False)
    createdAt = db.Column(db.Date,nullable=False)

    def __repr__(self):
        ccn = str(self.CardHolder + "'s Transaction")
        return ccn

db.create_all()

"""
# create serialization for fields
payment_fields = {
    'id': fields.Integer,
    'name': fields.String,

}
"""


#   check if required fields in request body of Payment method
paymentFields = reqparse.RequestParser()
paymentFields.add_argument("CreditCardNumber", type=str, help= "CreditCardNumber", required=True)
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder is required", required=True)
paymentFields.add_argument("ExpirationDate", type=str, help= "ExpirationDate is required", required=True)
paymentFields.add_argument("SecurityCode", type=str, help= "SecurityCode is required", required=True)
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder is required", required=True)
paymentFields.add_argument("Amount", type=float, help= "Amount is required", required=True)

class PaymentMethod(Resource):
    def post(self):
        args = paymentFields.parse_args()
        return {"data":args}

api.add_resource(PaymentMethod,"/payment")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)