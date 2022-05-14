import os
import requests
import telegram
import time
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__file__)


def check_works(dev_token):
    params = None
    while True:
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f'Token {dev_token}'
        }
        try:
            response = requests.get(
                url, headers=headers,
                params=params, timeout=10
            )
            response.raise_for_status()
            lesson_raw = response.json()
            if lesson_raw['status'] == 'timeout':
                params = {
                    'timestamp': str(lesson_raw['timestamp_to_request'])
                }
                continue
            else:
                for lesson in lesson_raw['new_attempts']:
                    lesson_name = lesson['lesson_title']
                    lesson_url = lesson['lesson_url']
                    if lesson['is_negative']:
                        text = f'Преподаватель проверил работу:\n{lesson_name}.\nУ вас нашлись ошибки.\nСсылка на работу: {lesson_url}'
                    else:
                        text = f'Преподаватель проверил работу:\n{lesson_name}.\nОшибок нет.\nСсылка на работу: {lesson_url}'
                    logger.debug(text)
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except Exception as error:
            logger.exception(error)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    dev_token = os.environ['DEVMAN_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']

    tg_bot = telegram.Bot(token=bot_token)
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_bot, chat_id))
    check_works(dev_token)
