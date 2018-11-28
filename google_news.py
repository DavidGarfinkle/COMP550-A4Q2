from secrets import API_KEY
import requests

ARTICLES_DIR = "./articles"

EVERYTHING_ENDPOINT = "https://newsapi.org/v2/everything"

TOPIC_KEYWORDS = {
    'ukraine': ('ukraine', 'russia'),
    'israel': ('israel', 'haredi', 'draft'),
    'trump': ('trump', 'mueller'),
    'tesla': ('elon', 'bankrupt', 'model 3')}

def get_cluster(topic):
    response = requests.get(EVERYTHING_ENDPOINT, auth


