from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime


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

    def __repr__(self):
        ccn = str(self.CardHolder + "'s Transaction")
        return ccn


# create serialization for fields
payment_fields = {
    'id': fields.Integer,
    'creditCardNumber': fields.String,
    'cardHolder': fields.String,
    'expiryDate': fields.String,
    'securityCode': fields.String,
    'amount':fields.Float,
    'createdAt': fields.String
}



#   check if required fields in request body of Payment method
paymentFields = reqparse.RequestParser()
paymentFields.add_argument("CreditCardNumber", type=str, help= "CreditCardNumber")
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder is required")
paymentFields.add_argument("ExpirationDate", type=str, help= "ExpirationDate is required")
paymentFields.add_argument("SecurityCode", type=str, help= "SecurityCode is required")
paymentFields.add_argument("Amount", type=float, help= "Amount is required")


class PaymentMethod(Resource):
    # serialize fields with marshal_with payment fields
    @marshal_with(payment_fields)

    # create post request for payment API
    def post(self):
        args = paymentFields.parse_args()

        date_time_obj = datetime.datetime.strptime(args['ExpirationDate'], '%Y-%m-%d')
        # create transaction record
        createdTransactionRecord = TransactionRecord(creditCardNumber=args['CreditCardNumber'], 
                                                    cardHolder=args['CardHolder'], expiryDate=date_time_obj,
                                                    securityCode=args['SecurityCode'], amount=args['Amount'])
        db.session.add(createdTransactionRecord)
        db.session.commit()
        return createdTransactionRecord, 200

api.add_resource(PaymentMethod,"/payment")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)