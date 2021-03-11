from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler)
from telegram import (ParseMode, Update)
from main_screen.texts import choose_text, welcome_text
from keyboards import menu_kb, back_to_menu_button


def new_user_callback(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text(welcome_text.format(username))
    context.chat_data.update({'url_section': {}})
    context.chat_data.update({'file_section': {}})
    context.chat_data.update({'short_text_section': {}})
    context.chat_data.update({'history_section': {}})

    menu_callback(update, context)


new_user_handler = CommandHandler(command='start',
                                  callback=new_user_callback,
                                  pass_chat_data=True,
                                  filters=Filters.private)


def menu_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text=choose_text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=menu_kb)

    return ConversationHandler.END


menu_handler = CommandHandler(command=['start', 'menu'],
                              callback=menu_callback,
                              pass_chat_data=True)

back_to_menu_handler = MessageHandler(callback=menu_callback,
                                      pass_chat_data=True,
                                      filters=Filters.regex('^{}'.format(back_to_menu_button)))

