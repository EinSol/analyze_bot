from main_screen.handlers import (new_user_handler, menu_handler)
from URL_screen.handlers import url_conversation_handler
from short_text_screen.handlers import short_text_conversation_handler
from telegram.ext import Updater
from decouple import config
import sentry_sdk
import logging
from logdna import LogDNAHandler
from sentry_sdk.integrations.logging import LoggingIntegration

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s')

logDNAoptions = dict()
logDNAoptions['index_meta'] = True
logDNAoptions['hostname'] = config('HOSTNAME', default='localhost')
logDNAhandler = LogDNAHandler(config('LOGDNA_KEY'), options=logDNAoptions)

logger = logging.getLogger()
logger.addHandler(logDNAhandler)

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)


sentry_sdk.init(
    config('SENTRY_URL'),
    traces_sample_rate=1.0,
    integrations=[sentry_logging]
)


class AnalyzeBot:
    def __init__(self, token: str):
        self.__api_token = token
        self.updater = Updater(token=self.__api_token)
        self.dispatcher = self.updater.dispatcher
        self.job_q = self.updater.job_queue


if __name__ == '__main__':
    env = config('ENV', default='DEBUG')

    bot = AnalyzeBot(config('BOT_TEST_TOKEN'))

    bot.dispatcher.add_handler(new_user_handler)
    bot.dispatcher.add_handler(menu_handler)
    bot.dispatcher.add_handler(url_conversation_handler)
    bot.dispatcher.add_handler(short_text_conversation_handler)

    bot.updater.start_polling()

    logging.info("Ready and listening for updates...")
    bot.updater.idle()
