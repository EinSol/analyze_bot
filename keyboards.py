from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


menu_keyboard = [['URl', 'Short text'],
                 ['File', 'History'],
                 ['Help']]

menu_kb = ReplyKeyboardMarkup(keyboard=menu_keyboard,
                              resize_keyboard=True,
                              one_time_keyboard=True)

extract_article_button = InlineKeyboardButton(text='Extract main parts of article(title, content, author etc.)',
                                              callback_data='extract_aricle')
summarize_button = InlineKeyboardButton(text='Summarize conntent',
                                        callback_data='summarize')
classify_button = InlineKeyboardButton(text='Classify content',
                                       callback_data='classify')
entity_button = InlineKeyboardButton(text='Extract entity',
                                     callback_data='entity')
to_file_button = InlineKeyboardButton(text='save in file',
                                      callback_data='save')

url_keyboard = [[extract_article_button],
                [summarize_button, classify_button],
                [entity_button, to_file_button]]

url_kb = InlineKeyboardMarkup(inline_keyboard=url_keyboard)

back_to_menu_button = '\U00002B05 Back to Menu'

back_to_menu_kb = ReplyKeyboardMarkup(keyboard=[[back_to_menu_button]],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)

