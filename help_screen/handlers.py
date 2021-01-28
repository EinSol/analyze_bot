from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler)
from telegram import (ParseMode, Update)
from keyboards import help_button
from help_screen.texts import help_text


def help_callback(update: Update, context: CallbackContext):
    cid = update.effective_message.chat.id
    q = update.message.text

    context.bot.send_message(chat_id=cid,
                             text=help_text,
                             parse_mode=ParseMode.HTML)


help_command_handler = CommandHandler(command=['help'],
                                      callback=help_callback,
                                      pass_chat_data=True)

help_handler = MessageHandler(callback=help_callback,
                              pass_chat_data=True,
                              filters=Filters.regex('^{}'.format(help_button)))




