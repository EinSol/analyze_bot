from telegram.ext import (MessageHandler, Filters, CallbackContext,
                          ConversationHandler )
from telegram import (ParseMode, Update)
from keyboards import back_to_menu_kb, menu_keyboard, kb_dict, back_to_menu_button, help_button
from help_screen.handlers import help_handler
from main_screen.handlers import back_to_menu_handler
from file_screen.texts import big_file_text, no_file_text, welcome_text, ask_text
from tools_handlers.handlers import (extract_entity_file_handler, extract_sentiment_file_handler,
                                     summarize_file_handler)

FILE_FUNCTIONS = range(1)


def file_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text=welcome_text,
                             reply_markup=back_to_menu_kb)
    return FILE_FUNCTIONS


file_handler = MessageHandler(callback=file_callback,
                              pass_chat_data=True,
                              filters=Filters.regex('{}'.format(menu_keyboard[1][0])))


def validate_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.document
    if q is None:
        update.message.reply_text(no_file_text)
        return

    q = q.to_dict()
    if q['file_size'] > 5*(10**7):
        update.message.reply_text(big_file_text)
        return

    context.chat_data.update({'query': q,
                              'update': update,
                              'current_section': 'file_section'})

    file_functions_callback(update, context)


validate_handler = MessageHandler(callback=validate_callback,
                                  pass_chat_data=True,
                                  filters=(Filters.all &
                                           ~Filters.regex(back_to_menu_button) &
                                           ~Filters.regex(help_button)))


def file_functions_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text
    section_name = context.chat_data['current_section']

    context.bot.send_message(chat_id=cid,
                             text=ask_text,
                             reply_markup=kb_dict[section_name])


file_conversation_handler = ConversationHandler(

    entry_points=[file_handler],

    states={

        FILE_FUNCTIONS: [
            validate_handler,
            extract_entity_file_handler,
            extract_sentiment_file_handler,
            summarize_file_handler,
            help_handler

        ]

    },

    fallbacks=[back_to_menu_handler],
    name='file',
    persistent=False
)