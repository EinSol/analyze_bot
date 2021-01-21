import requests
from decouple import config
from Tools.requests_url import (summarize_url, extract_article_url, entity_url,
                                sentiment_url, hashtag_url, classify_url)


class Toolkit:
    def __init__(self):
        self.__headers = {
            'x-rapidapi-key': config('API_KEY'),
            'x-rapidapi-host': config('API_HOST')
        }

    def response(self, url, params):
        res = requests.request('GET', url, headers=self.__headers, params=params)
        return res.json()

    def extract_article_info(self, querystring):
        search_url = querystring
        parameters = {'url': search_url}

        return self.response(extract_article_url, parameters)

    def summarize(self, querystring):
        title = querystring['title']
        length = querystring['length']
        text = querystring['text']
        text = text.replace('\n', '')
        search_url = querystring.get('url')

        parameters = {'title': title,
                      'text': text,
                      'url': search_url,
                      'length': 20}

        return self.response(summarize_url, parameters)

    def extract_entity(self, querystring):
        search_url = querystring.get('url')
        text = querystring['text']

        parameters = {'url':search_url,
                      'text':text}

        return self.response(entity_url, parameters)

    def extract_sentiment(self, querystring):
        search_url = querystring.get('url')
        text = querystring['text']
        mode = querystring['mode']

        parameters = {'url': search_url,
                      'text': text,
                      'mode': mode}

        return self.response(sentiment_url, parameters)

    def suggest_hashtag(self, querystring):
        search_url = querystring.get('url')
        text = querystring['text']

        parameters = {'url': search_url,
                      'text': text}

        return self.response(hashtag_url, parameters)

    def classify(self, querystring):
        search_url = querystring.get('url')
        text = querystring['text']

        parameters = {'url': search_url,
                      'text': text}

        return self.response(classify_url, parameters)

t = Toolkit()

