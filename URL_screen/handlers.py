from telegram.ext import (MessageHandler, Filters, CallbackContext,
                          CallbackQueryHandler, ConversationHandler, )
from telegram import (ParseMode, Update)
from keyboards import back_to_menu_kb, menu_keyboard, url_kb
from main_screen.handlers import back_to_menu_handler
from Tools.tools import Toolkit
import validators

URL_FUNCTIONS = range(1)


def url_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text='Enter URL on article.',
                             reply_markup=back_to_menu_kb)
    return URL_FUNCTIONS


url_handler = MessageHandler(callback=url_callback,
                             pass_update_queue=True,
                             pass_job_queue=True,
                             pass_chat_data=True,
                             filters=Filters.regex('{}'.format(menu_keyboard[0][0])))


def validate_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text
    print(q)
    if not validators.url(q):
        update.message.reply_text('Sorry, your url is not valid:(')
        return
    context.chat_data.update({'query': q,
                              'update': update})

    url_functions_callback(update, context)


validate_handler = MessageHandler(callback=validate_callback,
                                  pass_chat_data=True,
                                  filters=(Filters.text & ~Filters.regex('\U00002B05 Back to Menu')))


def url_functions_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text='What do you want to do?',
                             reply_markup=url_kb)


def summarize_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = context.chat_data['query']
    update = context.chat_data['update']
    storage_article = context.chat_data['url_section'].get(q)
    toolkit = Toolkit()

    if storage_article is not None:
        current_article = {'title': storage_article['title'],
             'url': storage_article['url'],
             'text': storage_article['text'],
             'length': 10}

    else:
        context.chat_data['url_section'].update({q: {'url': q}})
        article_info = toolkit.extract_article_info(q)
        print(article_info)
        if len(article_info['article']) > 5100:
            update.message.reply_text('Sorry, article is too big(>5100). \n Please, go back to menu and choose file section')
            return

        current_article = {'title': article_info['title'],
                            'text': article_info['article'],
                            'author': article_info['author'],
                            'date': article_info['publishDate'],
                            'tags': article_info['tags'],
                            'url': q,
                           'length': 10}

        context.chat_data['url_section'][q].update(current_article)

    summarized_sentences = current_article.get('sentences')

    if summarized_sentences is None:
        summarized_sentences = toolkit.summarize(current_article)['sentences']
        context.chat_data['url_section'][q].update({'sentences': summarized_sentences})

    convert_summarized_sentences = ''

    for index, value in enumerate(summarized_sentences):
        convert_summarized_sentences += f'{index}. {value}\n'
    context.bot.send_message(chat_id=cid,
                             text=convert_summarized_sentences,
                             reply_markup=url_kb)


summarize_handler = CallbackQueryHandler(callback=summarize_callback,
                                         pass_chat_data=True,
                                         pattern='summarize')


url_conversation_handler = ConversationHandler(

    entry_points=[url_handler],

    states={

        URL_FUNCTIONS: [
            validate_handler,
            summarize_handler
        ]

    },

    fallbacks=[back_to_menu_handler],
    name='URL',
    persistent=False
)