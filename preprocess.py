import os
import json

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk import word_tokenize
from nltk.tokenize import punkt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from config import *

stopwords = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
sent_detector = punkt.PunktSentenceTokenizer()

def tokenize(text):
    tokens = word_tokenize(text)

    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stopwords]

    return tokens

def attach_parsed_sentences(article):
    sentences = [s for s in sent_detector.tokenize(article['content'])]
    article['sentences'] = sentences

def attach_words(article):
    for index, sentence in enumerate(article['sentences']):
        words = tokenize(sentence)
        article['words'] = words
        article['words_to_sentences'] = [index] * len(words)

def main():
    for jsonfile in os.listdir(ARTICLES_DIR):
        filepath = os.path.join(ARTICLES_DIR, jsonfile)
        print("processing " + filepath)

        with open(filepath, 'r') as f:
            articles = json.loads(f.read())

            for article in articles:
                print("   " + article['title'])
                attach_parsed_sentences(article)
                attach_words(article)

        with open(filepath, 'w') as f:
            f.write(json.dumps(articles))

if __name__ == "__main__":
    main()
