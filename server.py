from flask import Flask, request, jsonify
from flask_api import status
from src.tf_check import tf_health_check
from src.libretto_bot import LibrettoBot
from gpt_2_finetuning.conditional_sample_model import ConditionalSampleModel
from src.sentiment_analysis import analyze


app = Flask(__name__)

model = ConditionalSampleModel(checkpoint_dir='./model', sample_length=50)
bot = LibrettoBot(model)


@app.route('/', methods=['GET'])
def health_check():
    return {'health': 'good'}, status.HTTP_200_OK


@app.route('/tf_check', methods=['GET'])
def tf_check():
    return tf_health_check()


@app.route('/gpt2', methods=['GET'])
def gpt2():
    prompt = request.args.get('prompt')
    bot.actor_prompt(prompt)
    return {'gpt2': bot.get_last_response(),
            'sentiment': analyze(bot.get_last_response())
        }


@app.route('/gpt2_mock', methods=['GET'])
def gpt2_mock():
    return {'gpt2': 'This is a mock response.',
            'sentiment': {
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0,
                    'compound': 0
            }
        }


if __name__ == '__main__':
    app.run(port=8000, debug=True)
