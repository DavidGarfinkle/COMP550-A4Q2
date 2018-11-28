import os
import json

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk import word_tokenize
from nltk.tokenize import punkt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from config import *

stopwords = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
sent_detector = punkt.PunktSentenceTokenizer()

stopwords.append([
    "image", "copyright", "caption"])

def tokenize(text):
    tokens = word_tokenize(text)

    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords]

    return tokens

def attach_parsed_sentences(article):
    sentences = [s for s in sent_detector.tokenize(article['content'])]
    article['sentences'] = sentences

def attach_words(article):
    article['words'] = []
    for index, sentence in enumerate(article['sentences']):
        words = tokenize(sentence)
        article['words'].append(words)

def preprocess_article(content_string):
    obj = {'content': content_string}
    attach_parsed_sentences(obj)
    attach_words(obj)
    return obj

def main():

    for doc in [d for d in os.listdir(ARTICLES_DIR) if os.path.splitext(d) == 'txt']:
        filepath = os.path.join(ARTICLES_DIR, doc)
        print("processing " + filepath)

        with open(filepath, 'r') as f:
            article = f.read()
            jsonobj = preprocess_article(article)

        json_filepath = os.path.splitext(filepath)[0] + '.json'
        print("writing processed article to {}".format(json_filepath))
        with open(json_filepath, 'w') as f:
            f.write(json.dumps(jsonobj))

if __name__ == "__main__":
    main()
