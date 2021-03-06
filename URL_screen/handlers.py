from telegram.ext import (MessageHandler, Filters, CallbackContext,
                          ConversationHandler)
from telegram import (ParseMode, Update)
from chattools import clean_chat
from keyboards import back_to_menu_kb, menu_keyboard, kb_dict, back_to_menu_button, help_button
from help_screen.handlers import help_handler
from main_screen.handlers import back_to_menu_handler
from URL_screen.texts import unvalid_text, welcome_text, ask_text
from tools_handlers.handlers import (summarize_handler, extract_sentiment_handler,
                                     extract_entity_handler, extract_article_handler)
import validators

URL_FUNCTIONS = range(1)


def url_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text=welcome_text,
                             reply_markup=back_to_menu_kb)
    return URL_FUNCTIONS


url_handler = MessageHandler(callback=url_callback,
                             pass_chat_data=True,
                             filters=Filters.regex('{}'.format(menu_keyboard[0][0])))


def validate_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text.lstrip().rstrip()

    clean_chat(update, context)

    if not validators.url(q):
        mid = update.message.reply_text(text=unvalid_text).message_id
        context.chat_data.update({'message_ids': [mid]})
        return
    context.chat_data.update({'query': q,
                              'update': update,
                              'current_section': 'url_section'})

    url_functions_callback(update, context)


validate_handler = MessageHandler(callback=validate_callback,
                                  pass_chat_data=True,
                                  filters=(Filters.text &
                                           ~Filters.regex(back_to_menu_button) &
                                           ~Filters.regex(help_button)))


def url_functions_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text
    section_name = context.chat_data['current_section']

    mid = context.bot.send_message(chat_id=cid,
                                   text=ask_text,
                                   reply_markup=kb_dict[section_name]).message_id

    context.chat_data.update({'message_ids': [mid]})


url_conversation_handler = ConversationHandler(

    entry_points=[url_handler],

    states={

        URL_FUNCTIONS: [
            validate_handler,
            summarize_handler,
            extract_article_handler,
            extract_entity_handler,
            extract_sentiment_handler,
            help_handler

        ]

    },
    fallbacks=[back_to_menu_handler],
    name='url',
    persistent=False
)
