import os
import json
from config import *
from newsapi import NewsApiClient
from newspaper import Article

from secrets import API_KEY

newsapi = NewsApiClient(api_key = API_KEY)

def get_cluster(topic, query):
    cluster = newsapi.get_everything(
            q=query,
            sort_by="relevancy")

    # Top-level response has metadata
    # We are only interested in the articles
    gn_items = cluster['articles']

    try:
        gn_items = process_cluster(gn_items)
    except Exception:
        print("Failed to process topic {}".format(topic))

    return gn_items

def process_cluster(gn_items):

    # Take the first ten hits
    gn_items = gn_items[:MIN_ARTICLE_HITS]

    # For each item, attach article content to ['content'] attribute 
    for item in gn_items:
        attach_article_content(item, 'content')

    # Filter the google news items
    gn_items = filter_cluster(gn_items)

    if (len(gn_items) < MIN_ARTICLE_HITS):
        raise Exception("Not enough article hits")

    return gn_items

def attach_article_content(gn_item, dctkey):
    article = Article(gn_item['url'])
    print("   downloading {}".format(gn_item['url']))

    try:
        article.download()
        article.parse()
        gn_item[dctkey] = article.text
    except Exception:
        print("   Article.py failed to download or parse article")
        gn_item[dctkey] = ""

def filter_cluster(cluster):
    def by_length(gn_item):
        return len(gn_item['content'] or []) >= MIN_ARTICLE_CHARACTER_LENGTH

    def filter_all(gn_item):
        return by_length(gn_item)

    return list(filter(filter_all, cluster))

def main():
    for topic, phrase in TOPIC_KEYWORDS.items():
        print("getting articles for (topic, phrase_query): ({}, {})".format(topic, phrase))
        gn_items = get_cluster(topic, phrase)
        if not gn_items:
            continue

        output_path = os.path.join(ARTICLES_DIR, "{}.json".format(topic))
        print("writing {} articles to {}".format(len(gn_items), output_path))
        with open(output_path, 'w') as f:
            f.write(json.dumps(gn_items))


if __name__ == '__main__':
    main()
