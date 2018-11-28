import os

ARTICLES_DIR = "./docs"
MIN_ARTICLE_CHARACTER_LENGTH = 3000
MIN_ARTICLE_HITS = 3
MAX_CLUSTER_SIZE = 4
MAX_SUMMARY_SIZE = 100

TOPIC_KEYWORDS = {
    'ukraine': 'ukraine russia',
    'israel': 'israel haredi draft',
    'trump': 'trump mueller',
    'tesla': 'elon bankrupt model 3'}

def DOC_PATH(clusterNum, articleNum):
    return os.path.join(ARTICLES_DIR, "doc{}-{}.txt".format(clusterNum, articleNum))
