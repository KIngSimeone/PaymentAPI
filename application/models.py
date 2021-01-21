from sqlalchemy import Column, Integer, String, ForeignKey, Date,
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from datetime import datetime
import app

db = app.db
migrate = app.migrate



class Transaction(Model):
    id = db.Column(Integer, primary_key=True)
    creditCardNumber =  db.Column(String(150), unique = True, nullable=False)
    cardHolder =  db.Column(String(564))
    expiryDate = db.Column(Date)
    securityCode = db.Column(String(20))
    createdAt = db.Column(datetime)

    def __str__(self):
        ccn = self.creditCardNumber
        return ccn