import requests
from decouple import config
from docx import Document
import os
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
        title = querystring.get('title')
        length = querystring.get('length', 10)
        text = querystring.get('text')
        search_url = querystring.get('url')

        parameters = {'title': title,
                      'text': text,
                      'url': search_url,
                      'length': length}

        return self.response(summarize_url, parameters)

    def extract_entity(self, querystring):
        search_url = querystring.get('url')
        text = querystring.get('text')

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

    def create_document(self, querystring):
        title = querystring.get('title')
        text = querystring.get('text')
        document = Document()
        document.add_heading('Analyze results', 0)

        for key, value in querystring.items():
            document.add_heading(key, level=1)
            if type(value) == list:
                for subvalue in value:
                    document.add_paragraph(
                        subvalue, style='List Bullet'
                        )
                continue
            document.add_paragraph(value)

        path = os.getcwd()
        document.save(f'{path}/doc_storage/ent-ffef.docx')

        return 'ffef'
























# document = Document()
#
#
#
# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True
#
# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )
#
#
# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )
#
# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc
#
# document.add_page_break()
#
# document.save('demo.docx')
