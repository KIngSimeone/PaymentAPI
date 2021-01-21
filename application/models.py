from sqlalchemy import Column, Integer, String, ForeignKey, Date,
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from datetime import datetime
import app


class Transaction(Model):
    id = Column(Integer, primary_key=True)
    creditCardNumber =  Column(String(150), unique = True, nullable=False)
    cardHolder =  Column(String(564))
    expiryDate = Column(Date)
    securityCode = Column(String(20))
    createdAt = Column(datetime)

    def __str__(self):
        ccn = self.creditCardNumber
        return ccn