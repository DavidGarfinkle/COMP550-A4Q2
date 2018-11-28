"""
Expects article json objects

content --- the raw text
sentences --- tokenized sentences of the text
words --- lemmatized and tokenized words of the text, not necessarily unique
words_to_sentences --- map from each word to the sentence it occurs in
"""
import sys
import os
import json
from collections import Counter
from preprocess import preprocess_article
from config import *

WORDS_TO_SENTENCES = {}

def stepone(article_obj):
    words = [w for lst in article_obj['words'] for w in lst]
    word_counts = Counter(words)
    word_probabilities = { word: float(word_counts[word]) / sum(word_counts.values()) for word in word_counts }

    return word_probabilities

def steptwo(article_obj, word_probabilities):
    sentence_weights = {}

    for sentence_index, sentence in enumerate(article_obj['words']):
        summed_word_probability = sum(word_probabilities[word] for word in sentence)
        sentence_weights[sentence_index] = summed_word_probability / float(len(sentence))

    return sentence_weights

def stepthree(article_obj, word_probabilities, sentence_weights):
    maxword = max(word_probabilities, key = lambda w: word_probabilities[w])

    maxword_sentences = [s_index for s_index in sentence_weights if maxword in article_obj['words'][s_index]]
    best_sentence_index = max(maxword_sentences, key = lambda s_index: article_obj['words'][s_index])

    return best_sentence_index


def stepfour(article_obj, word_probabilities, s_index):
    for word in article_obj['words'][s_index]:
        word_probabilities[word] *= word_probabilities[word]

def get_summary(article_obj, summary_indices):
    return ". ".join(article_obj['sentences'][s_index] for s_index in summary_indices)

def orig(article_obj):

    word_probabilities = stepone(article_obj)
    summary_indices = []

    while len(get_summary(article_obj, summary_indices).split(' ')) < 100:
        sentence_weights = steptwo(article_obj, word_probabilities)

        s_index = stepthree(article_obj, word_probabilities, sentence_weights)
        summary_indices.append(s_index)

        stepfour(article_obj, word_probabilities, s_index)

    return summary_indices

def main(docpath):

    with open(docpath, 'r') as f:
        article = f.read()

    article_obj = preprocess_article(article)

    summary_indices = orig(article_obj)

    summary = get_summary(article_obj, summary_indices)


    print(summary)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python sumbasic.py <method_name> <file_n>*")
        sys.exit(1)

    method = sys.argv[1]
    docpath = sys.argv[2]

    main(docpath)
