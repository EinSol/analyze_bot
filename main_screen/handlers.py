from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler)
from telegram import (ParseMode, Update)
from keyboards import menu_kb, back_to_menu_button

MENU = range(1)


def new_user_callback(update: Update, context: CallbackContext):
    update.message.reply_text(text='Welcome Stranger!')
    menu_callback(update, context)
    context.chat_data.update({'url_section': {}})
    context.chat_data.update({'file_section': {}})
    context.chat_data.update({'short_text_section': {}})
    context.chat_data.update({'history_section': {}})

    return MENU


new_user_handler = CommandHandler(command='start',
                                  callback=new_user_callback,
                                  pass_chat_data=True,
                                  filters=Filters.private)


def menu_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text='Choose text type:',
                             parse_mode=ParseMode.HTML,
                             reply_markup=menu_kb)

    return ConversationHandler.END


menu_handler = CommandHandler(command=['start'],
                              callback=menu_callback,
                              pass_chat_data=True)

back_to_menu_handler = MessageHandler(callback=menu_callback,
                                      pass_chat_data=True,
                                      filters=Filters.regex('^{}'.format(back_to_menu_button)))

