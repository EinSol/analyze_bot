from telegram.ext import ( CallbackContext, CallbackQueryHandler)
from telegram import (ParseMode, Update)
from keyboards import kb_dict
from Tools.tools import Toolkit, get_parts_of_text
from tools_handlers.texts import (sentiment_text, summarize_text, hashtags_text,
                                  categories_text, categories_title, hashtags_title,
                                  sentiment_title, summarize_title, error_text, nothing_text)
import os
import textract
import validators


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

    context.chat_data[section_name][q].update({'extract_article_file': file_id})
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
        if validators.url(q):
            context.chat_data[section_name].update({q: {'url': q}})
            article_info = toolkit.extract_entity({'url': q})['entities']
        else:
            context.chat_data[section_name].update({q: {'text': q}})
            article_info = toolkit.extract_entity({'text': q})['entities']
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
        if validators.url(q):
            context.chat_data[section_name].update({q: {'url': q}})
            article_info = toolkit.extract_sentiment({'url': q})
        else:
            context.chat_data[section_name].update({q: {'text': q}})
            article_info = toolkit.extract_sentiment({'text': q})

        current_article = {'polarity': article_info['polarity'],
                           'polarity_confidence': article_info['polarity_confidence'],
                           'subjectivity': article_info['subjectivity'],
                           'subjectivity_confidence': article_info['subjectivity_confidence']
                           }

        context.chat_data[section_name][q].update(current_article)

    summarize_sentiment = sentiment_title
    for key, value in current_article.items():
        key = key.replace('_', ' ')
        summarize_sentiment += sentiment_text.format(key, value)

    context.bot.send_message(chat_id=cid,
                             text=summarize_sentiment,
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

    convert_summarized_sentences = summarize_title

    for index, value in enumerate(summarized_sentences):
        convert_summarized_sentences += summarize_text.format(index+1, value)

    context.bot.send_message(chat_id=cid,
                             text=convert_summarized_sentences,
                             parse_mode=ParseMode.HTML,
                             reply_markup=kb_dict[section_name])


summarize_handler = CallbackQueryHandler(callback=summarize_callback,
                                         pass_chat_data=True,
                                         pattern='summarize')


def hashtag_callback(update: Update, context: CallbackContext):

    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('hashtags'):
        current_article = storage_article

    else:
        if validators.url(q):
            context.chat_data[section_name].update({q: {'url': q}})
            current_article = {'url': q}
        else:
            context.chat_data[section_name].update({q: {'text': q}})
            current_article = {'text': q}

    summarized_hashtags = current_article.get('hashtags')

    if summarized_hashtags is None:
        summarized_hashtags = toolkit.suggest_hashtag(current_article)['hashtags']
        context.chat_data[section_name][q].update({'hashtags': summarized_hashtags})

    convert_summarized_hashtags = hashtags_title

    for index, value in enumerate(summarized_hashtags):
        convert_summarized_hashtags += hashtags_text.format(index+1, value)

    convert_summarized_hashtags += f'\n{"".join(summarized_hashtags)}'
    print(convert_summarized_hashtags)
    context.bot.send_message(chat_id=cid,
                             text=convert_summarized_hashtags,
                             parse_mode=ParseMode.HTML,
                             reply_markup=kb_dict[section_name],
                             )


hashtag_handler = CallbackQueryHandler(callback=hashtag_callback,
                                       pass_chat_data=True,
                                       pattern='hashtag')


def classify_callback(update: Update, context: CallbackContext):

    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(q)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('categories'):
        current_article = storage_article

    else:
        if validators.url(q):
            context.chat_data[section_name].update({q: {'url': q}})
            current_article = {'url': q}
        else:
            context.chat_data[section_name].update({q: {'text': q}})
            current_article = {'text': q}

    summarized_categories = current_article.get('categories')

    if summarized_categories is None:
        summarized_categories = toolkit.classify(current_article)['categories']
        context.chat_data[section_name][q].update({'categories': summarized_categories})

    convert_summarized_categories = categories_title

    if not summarized_categories:
        context.bot.send_message(chat_id=cid,
                                 text=nothing_text,
                                 parse_mode=ParseMode.HTML)
        return

    print(summarized_categories)
    for index, value in enumerate(summarized_categories):
        convert_summarized_categories += categories_text.format(index+1,
                                                                value['label'],
                                                                value['confidence'])

    convert_summarized_categories += f'\n{"".join(summarized_categories)}'

    context.bot.send_message(chat_id=cid,
                             text=convert_summarized_categories,
                             reply_markup=kb_dict[section_name],
                             parse_mode=ParseMode.HTML)


classify_handler = CallbackQueryHandler(callback=classify_callback,
                                        pass_chat_data=True,
                                        pattern='classify')


def extract_entity_file_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    file_name = q['file_name']
    file_id = q['file_id']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(file_name)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('entity_file'):
        context.bot.send_document(chat_id=cid,
                                  document=storage_article.get('entity_file'),
                                  reply_markup=kb_dict[section_name])
        return

    path = f'{os.getcwd()}/doc_storage/{file_name}'

    with open(path, 'wb') as f:
        context.bot.get_file(file_id).download(out=f)
    content = str(textract.process(path))[2:]

    context.chat_data[section_name].update({file_name: {'file_id': file_id}})
    current_article = {'text': content}
    os.remove(path)

    text_parts, title = get_parts_of_text(current_article['text'])
    summarize_entities = {}
    for part in text_parts:
        try:
            part_entity = toolkit.extract_entity({'text': part,
                                                  'title': title})['entities']
        except:
            update.message.replu_text(error_text)

        for name, value in part_entity.items():
            if summarize_entities.get(name):
                summarize_entities[name] = list(set(summarize_entities[name] + value))
            else:
                summarize_entities.update({name: value})


    name = f'file_extract_entity_{cid}'
    path = toolkit.create_document(summarize_entities, name)

    file_id = context.bot.send_document(chat_id=cid,
                                        document=open(path, 'rb'),
                                        reply_markup=kb_dict[section_name]).document.file_id

    context.chat_data[section_name][file_name].update({'entity_file': file_id})
    os.remove(path)


extract_entity_file_handler = CallbackQueryHandler(callback=extract_entity_file_callback,
                                                   pass_chat_data=True,
                                                   pattern='entity')


def extract_sentiment_file_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    file_name = q['file_name']
    file_id = q['file_id']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(file_name)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('polarity'):
        current_article = {'polarity': storage_article['polarity'],
                           'polarity_confidence': storage_article['polarity_confidence'],
                           'subjectivity': storage_article['subjectivity'],
                           'subjectivity_confidence': storage_article['subjectivity_confidence']
                           }

    else:
        path = f'{os.getcwd()}/doc_storage/{file_name}'

        with open(path, 'wb') as f:
            context.bot.get_file(file_id).download(out=f)
        content = str(textract.process(path))[:5000]

        context.chat_data[section_name].update({file_name: {'file_id': file_id}})

        article_info = toolkit.extract_sentiment({'text': content})

        current_article = {'polarity': article_info['polarity'],
                           'polarity_confidence': article_info['polarity_confidence'],
                           'subjectivity': article_info['subjectivity'],
                           'subjectivity_confidence': article_info['subjectivity_confidence']
                           }

        os.remove(path)

        context.chat_data[section_name][file_name].update(current_article)

    summarize_sentiment = sentiment_title
    for key, value in current_article.items():
        key = key.replace('_', ' ')
        summarize_sentiment += sentiment_text.format(key, value)

    context.bot.send_message(chat_id=cid,
                             text=summarize_sentiment,
                             reply_markup=kb_dict[section_name],
                             parse_mode=ParseMode.HTML)


extract_sentiment_file_handler = CallbackQueryHandler(callback=extract_sentiment_file_callback,
                                                      pass_chat_data=True,
                                                      pattern='sentiment')


def summarize_file_callback(update: Update, context: CallbackContext):
    update = context.chat_data['update']
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    file_name = q['file_name']
    file_id = q['file_id']
    section_name = context.chat_data['current_section']
    storage_article = context.chat_data[section_name].get(file_name)
    toolkit = Toolkit()

    if storage_article is not None and storage_article.get('sentences'):
        current_article = storage_article

    else:
        path = f'{os.getcwd()}/doc_storage/{file_name}'

        with open(path, 'wb') as f:
            context.bot.get_file(file_id).download(out=f)
        content = str(textract.process(path))[2:]

        context.chat_data[section_name].update({file_name: {'file_id': file_id}})
        current_article = {'text': content}
        os.remove(path)

    summarized_sentences = current_article.get('sentences', [])

    if not summarized_sentences:
        text_parts, title = get_parts_of_text(current_article['text'])

        for part in text_parts:
            print(f'part###################{part}')
            try:
                summarized_sentences += toolkit.summarize({'text': part,
                                                           'title': title})['sentences']
            except:
                update.message.replu_text(error_text)

        context.chat_data[section_name][file_name].update({'sentences': summarized_sentences})

    name = f'file_summarize_{cid}'
    path = toolkit.create_document({'sentences': summarized_sentences}, name)

    sumarrize_file_id = context.bot.send_document(chat_id=cid,
                                                  document=open(path, 'rb'),
                                                  reply_markup=kb_dict[section_name]).document.file_id

    context.chat_data[section_name][file_name].update({'summarize_file': sumarrize_file_id})
    os.remove(path)


summarize_file_handler = CallbackQueryHandler(callback=summarize_file_callback,
                                              pass_chat_data=True,
                                              pattern='summarize')
