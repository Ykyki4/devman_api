import time
import textwrap
import logging
import os

import telegram
import requests


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_info_message(attempt):
    if attempt["is_negative"]:
        result_text = 'К сожалению в работе нашлись ошибки.'
    else:
        result_text = 'Преподавателю всё понравилось, можно приступать к работе.'
    text = textwrap.dedent(f'''\
    Вашу работу {attempt['lesson_title']} проверил преподаватель.
        
    Ссылка на работу: {attempt['lesson_url']}
            
    {result_text}
    ''')
    bot.send_message(chat_id=tg_chat_id, text=text)


if __name__ == '__main__':
    tg_token = os.environ['TG_TOKEN']
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']

    bot = telegram.Bot(token=tg_token)

    logger = logging.getLogger('Telegram Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))

    logger.info('Бот запущен')

    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    url = 'https://dvmn.org/api/long_polling/'
    params = {}
    while True:
        try:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                time.sleep(5)
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                continue
            except requests.exceptions.ReadTimeout:
                continue

            works = response.json()
            if works['status'] == 'timeout':
                params['timestamp'] = works['timestamp_to_request']
            if works['status'] == 'found':
                params['timestamp'] = works['last_attempt_timestamp']
                attempt = works["new_attempts"][0]
                send_info_message(attempt)
        except Exception:
            logger.exception('Бот упал с ошибкой:')
