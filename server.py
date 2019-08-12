from flask import Flask, request, jsonify
from flask_api import status

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return {'health': 'good'}, status.HTTP_200_OK


@app.route('/test', methods=['GET'])
def test_route():
    return 'hello_world'


if __name__ == '__main__':
    app.run(port=8000, debug=True)
