from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)