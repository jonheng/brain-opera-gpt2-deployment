from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test_route():
    return 'hello_world'


if __name__ == '__main__':
    app.run(port=8000, debug=True)
