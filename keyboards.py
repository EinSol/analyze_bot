from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


menu_keyboard = [['URl', 'Short text'],
                 ['File', 'Help']]

menu_kb = ReplyKeyboardMarkup(keyboard=menu_keyboard,
                              resize_keyboard=True,
                              one_time_keyboard=True)

extract_article_button = InlineKeyboardButton(text='Extract article',
                                              callback_data='extract_article')
summarize_button = InlineKeyboardButton(text='Summarize content',
                                        callback_data='summarize')
classify_button = InlineKeyboardButton(text='Classify content',
                                       callback_data='classify')
entity_button = InlineKeyboardButton(text='Extract entity',
                                     callback_data='entity')
sentiment_button = InlineKeyboardButton(text='Extract sentiment',
                                        callback_data='sentiment')
hashtag_button = InlineKeyboardButton(text='suggest hashtags',
                                      callback_data='hashtag')


url_keyboard = [[extract_article_button, entity_button],
                [summarize_button, sentiment_button]]

short_text_keyboard = [[entity_button, sentiment_button],
                       [hashtag_button, classify_button]]

file_keyboard = [[summarize_button, sentiment_button],
                 [entity_button]]


kb_dict = {'url_section': InlineKeyboardMarkup(inline_keyboard=url_keyboard),
           'short_text_section': InlineKeyboardMarkup(inline_keyboard=short_text_keyboard),
           'file_section': InlineKeyboardMarkup(inline_keyboard=file_keyboard)}

back_to_menu_button = '\U00002B05 Back to Menu'

back_to_menu_kb = ReplyKeyboardMarkup(keyboard=[[back_to_menu_button]],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)


