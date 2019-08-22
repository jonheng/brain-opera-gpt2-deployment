import gpt_2_simple as gpt2
from flask import Flask, request, jsonify
from flask_api import status
from tf_check import tf_health_check
from gpt2_model import get_single_response

app = Flask(__name__)

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)


@app.route('/', methods=['GET'])
def health_check():
    return {'health': 'good'}, status.HTTP_200_OK


@app.route('/tf_check', methods=['GET'])
def tf_check():
    return tf_health_check()


@app.route('/gpt2', methods=['GET'])
def gpt2():
    prompt = request.args.get('prompt')
    return get_single_response(sess, prompt)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
