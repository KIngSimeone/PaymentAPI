from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.py')




@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)