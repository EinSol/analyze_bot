from telegram.ext import (MessageHandler, Filters, CallbackContext,
                          ConversationHandler)
from telegram import (Update)
from chattools import clean_chat
from keyboards import back_to_menu_kb, menu_keyboard, kb_dict, back_to_menu_button, help_button
from main_screen.handlers import back_to_menu_handler
from help_screen.handlers import help_handler
from short_text_screen.texts import unvalid_text, big_text, welcome_text, ask_text
from tools_handlers.handlers import (extract_sentiment_handler, classify_handler,
                                     extract_entity_handler, hashtag_handler)
import validators

SHORT_TEXT_FUNCTIONS = range(1)


def short_text_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text=welcome_text,
                             reply_markup=back_to_menu_kb)
    return SHORT_TEXT_FUNCTIONS


short_text_handler = MessageHandler(callback=short_text_callback,
                                    pass_chat_data=True,
                                    filters=Filters.regex('{}'.format(menu_keyboard[0][1])))


def validate_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text.lstrip().rstrip()

    clean_chat(update, context)

    if len(q) > 500:
        mid = update.message.reply_text(big_text)
        context.chat_data.update({'message_ids': [mid]})
        return

    if not validators.url(q) and len(q.split(' ')) == 1:
        mid = update.message.reply_text(unvalid_text)
        context.chat_data.update({'message_ids': [mid]})
        return

    context.chat_data.update({'query': q,
                              'update': update,
                              'current_section': 'short_text_section'})

    short_text_functions_callback(update, context)


validate_handler = MessageHandler(callback=validate_callback,
                                  pass_chat_data=True,
                                  filters=(Filters.text &
                                           ~Filters.regex(back_to_menu_button) &
                                           ~Filters.regex(help_button)))


def short_text_functions_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text
    section_name = context.chat_data['current_section']

    mid = context.bot.send_message(chat_id=cid,
                                   text=ask_text,
                                   reply_markup=kb_dict[section_name])

    context.chat_data.update({'message_ids': [mid]})


short_text_conversation_handler = ConversationHandler(

    entry_points=[short_text_handler],

    states={

        SHORT_TEXT_FUNCTIONS: [
            validate_handler,
            extract_entity_handler,
            extract_sentiment_handler,
            hashtag_handler,
            classify_handler,
            help_handler
        ]

    },

    fallbacks=[back_to_menu_handler],
    name='short_text',
    persistent=False
)
