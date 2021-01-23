from telegram.ext import (MessageHandler, Filters, CallbackContext,
                        ConversationHandler )
from telegram import (ParseMode, Update)
from keyboards import back_to_menu_kb, menu_keyboard, kb_dict
from main_screen.handlers import back_to_menu_handler
from URL_screen.texts import unvalid_text
from tools_handlers.handlers import (summarize_handler, extract_sentiment_handler,
                                     extract_entity_handler, extract_article_handler)
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
                             pass_chat_data=True,
                             filters=Filters.regex('{}'.format(menu_keyboard[0][0])))


def validate_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text.lstrip().rstrip()

    if not validators.url(q):
        update.message.reply_text(text=unvalid_text)
        return
    context.chat_data.update({'query': q,
                              'update': update,
                              'current_section': 'url_section'})

    url_functions_callback(update, context)


validate_handler = MessageHandler(callback=validate_callback,
                                  pass_chat_data=True,
                                  filters=(Filters.text & ~Filters.regex('\U00002B05 Back to Menu')))


def url_functions_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text
    section_name = context.chat_data['current_section']

    context.bot.send_message(chat_id=cid,
                             text='What do you want to do?',
                             reply_markup=kb_dict[section_name])


url_conversation_handler = ConversationHandler(

    entry_points=[url_handler],

    states={

        URL_FUNCTIONS: [
            validate_handler,
            summarize_handler,
            extract_article_handler,
            extract_entity_handler,
            extract_sentiment_handler

        ]

    },
    fallbacks=[back_to_menu_handler],
    name='URL',
    persistent=False
)

