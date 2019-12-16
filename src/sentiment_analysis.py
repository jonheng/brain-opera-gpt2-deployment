import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sentimentIntensityAnalyzer = SentimentIntensityAnalyzer()


def analyze(sentence):
    return sentimentIntensityAnalyzer.polarity_scores(sentence)
