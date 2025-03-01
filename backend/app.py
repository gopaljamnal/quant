from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/greet', methods=["GET"])
@cross_origin()
def greet():
    return jsonify({'message': 'Hello World from Flask!'})


if __name__ == '__main__':
    app.run(debug=True)