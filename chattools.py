
from telegram import Update
from telegram.ext import callbackcontext


def clean_chat(update: Update, context: callbackcontext):

    if 'message_ids' in context.chat_data.keys():

        cid = update.effective_message.chat.id

        for mid in context.chat_data['message_ids']:
            try:
                context.bot.delete_message(chat_id=cid,
                                           message_id=mid)
            except Exception as e:
                print(e)

    if 'file_ids' in context.chat_data.keys():
        cid = update.effective_message.chat.id

        for mid in context.chat_data['file_ids']:
            try:
                context.bot.edit_message_reply_markup(message_id=mid,
                                                      chat_id=cid,
                                                      reply_markup=None)
            except Exception as e:
                print(e)

    context.chat_data['message_ids'] = list()
    context.chat_data['file_ids'] = list()


