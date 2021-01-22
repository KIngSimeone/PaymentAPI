from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
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
    creditCardNumber =  db.Column(db.String(100),nullable=False)
    cardHolder =  db.Column(db.String(564),nullable=False)
    expiryDate = db.Column(db.Date,nullable=False)
    securityCode = db.Column(db.String(20),nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paymentGateway=db.Column(db.String(100), nullable=False)

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
    'paymentGateway':fields.String
}


#   check if required fields in request body of Payment method
paymentFields = reqparse.RequestParser()
paymentFields.add_argument("CreditCardNumber", type=str, help= "CreditCardNumber", required=True)
paymentFields.add_argument("CardHolder", type=str, help= "CardHolder is required", required=True)
paymentFields.add_argument("ExpirationDate", type=str, help= "ExpirationDate is required", required=True)
paymentFields.add_argument("SecurityCode", type=str, help= "SecurityCode is required")
paymentFields.add_argument("Amount", type=float, help= "Amount is required", required=True)


class PaymentMethod(Resource):
    # serialize fields with marshal_with payment fields
    @marshal_with(payment_fields)

    # create post request for payment API
    def post(self):
        args = paymentFields.parse_args()

        # covert inputed string to date format
        exdate = datetime.datetime.strptime(args['ExpirationDate'], '%Y-%m-%d')

        # check if exdate is in the past by comparing with present date
        present = datetime.datetime.now()
        if exdate < present:
            abort(400, message="Your Date is in the past, please select dat in future")

        # check if security code is more than 3 characters
        if len(args['SecurityCode']) > 3:
            abort(400, message="Your security code contains more than 3 characters")
        
        # check if amount is negative
        if args['Amount'] < 0:
            abort(400, message="Amount cannot be negative number")

        #Select Payment gateway
        if args['Amount'] < 20:
            paymentgateway="CheapPaymentGateway"

        if args['Amount'] >= 20 and args['Amount'] <= 500:
            paymentgateway="ExpensivePaymentGateway"

        if args['Amount'] > 500:
            paymentgateway="PremiumPaymentGateway"


        # create transaction record
        createdTransactionRecord = TransactionRecord(creditCardNumber=args['CreditCardNumber'], 
                                                    cardHolder=args['CardHolder'], expiryDate=exdate,
                                                    securityCode=args['SecurityCode'], amount=args['Amount'],
                                                    paymentGateway=paymentgateway)
        db.session.add(createdTransactionRecord)
        db.session.commit()
        return createdTransactionRecord, 200

# Add PaymentGateway as api resource
api.add_resource(PaymentMethod,"/payment")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)