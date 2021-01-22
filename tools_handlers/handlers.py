from telegram.ext import ( CallbackContext, CallbackQueryHandler)
from telegram import (ParseMode, Update)
from keyboards import kb_dict
from Tools.tools import Toolkit
from tools_handlers.texts import sentiment_text, summarize_text
import os


def extract_article_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)

    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('extract_article_file'):
        context.bot.send_document(chat_id=cid,
                                  document=storage_article.get('extract_article_file'),
                                  reply_markup=kb_dict[section_name])
        print('send archive')
        return

    else:
        context.chat_data[section_name].update({q: {'url': q}})
        article_info = toolkit.extract_article_info(q)

        current_article = {'title': article_info['title'],
                           'text': article_info['article'],
                           'author': article_info['author'],
                           'date': article_info['publishDate'],
                           'tags': article_info['tags']
                           }

    name = f'url_extract_article_{cid}'
    path = toolkit.create_document(current_article, name)

    file_id = context.bot.send_document(chat_id=cid,
                                        document=open(path, 'rb'),
                                        reply_markup=kb_dict[section_name]).document.file_id

    context.chat_data[section_name][q].update({'extract_article_callback': file_id})
    os.remove(path)


extract_article_handler = CallbackQueryHandler(callback=extract_article_callback,
                                               pass_chat_data=True,
                                               pattern='extract_article')


def extract_entity_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('entity_file'):
        context.bot.send_document(chat_id=cid,
                                  document=storage_article.get('entity_file'),
                                  reply_markup=kb_dict[section_name])
        return

    else:
        context.chat_data[section_name].update({q: {'url': q}})
        article_info = toolkit.extract_entity({'url': q})['entities']

        current_article = article_info

    name = f'url_extract_entity_{cid}'
    path = toolkit.create_document(current_article, name)

    file_id = context.bot.send_document(chat_id=cid,
                                        document=open(path, 'rb'),
                                        reply_markup=kb_dict[section_name]).document.file_id

    context.chat_data[section_name][q].update({'entity_file': file_id})
    os.remove(path)


extract_entity_handler = CallbackQueryHandler(callback=extract_entity_callback,
                                              pass_chat_data=True,
                                              pattern='entity')


def extract_sentiment_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('polarity'):
        current_article = {'polarity': storage_article['polarity'],
                           'polarity_confidence': storage_article['polarity_confidence'],
                           'subjectivity': storage_article['subjectivity'],
                           'subjectivity_confidence': storage_article['subjectivity_confidence']
                           }

    else:
        context.chat_data[section_name].update({q: {'url': q}})
        article_info = toolkit.extract_sentiment({'url': q,
                                                  'mode': 'document'})

        current_article = {'polarity': article_info['polarity'],
                           'polarity_confidence': article_info['polarity_confidence'],
                           'subjectivity': article_info['subjectivity'],
                           'subjectivity_confidence': article_info['subjectivity_confidence']
                           }

        context.chat_data[section_name][q].update(current_article)

    summarized_result = ''
    for key, value in current_article.items():
        key = key.replace('_', ' ')
        summarized_result += sentiment_text.format(key, value)

    context.bot.send_message(chat_id=cid,
                             text=summarized_result,
                             reply_markup=kb_dict[section_name],
                             parse_mode=ParseMode.HTML)


extract_sentiment_handler = CallbackQueryHandler(callback=extract_sentiment_callback,
                                                 pass_chat_data=True,
                                                 pattern='sentiment')


def summarize_callback(update: Update, context: CallbackContext):

    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('sentences'):
        current_article = storage_article

    else:
        context.chat_data[section_name].update({q: {'url': q}})
        current_article = {'url': q}

    summarized_sentences = current_article.get('sentences')

    if summarized_sentences is None:
        summarized_sentences = toolkit.summarize(current_article)['sentences']
        context.chat_data[section_name][q].update({'sentences': summarized_sentences})

    convert_summarized_sentences = ''

    for index, value in enumerate(summarized_sentences):
        convert_summarized_sentences += summarize_text.format(index+1, value)

    context.bot.send_message(chat_id=cid,
                             text=convert_summarized_sentences,
                             reply_markup=kb_dict[section_name])


summarize_handler = CallbackQueryHandler(callback=summarize_callback,
                                         pass_chat_data=True,
                                         pattern='summarize')
