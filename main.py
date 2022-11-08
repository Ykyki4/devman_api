import time

import telegram
import requests
from environs import Env


def send_info_message(attempt):
    if attempt["is_negative"]:
        is_right = 'К сожалению в работе нашлись ошибки.'
    else:
        is_right = 'Преподавателю всё понравилось, можно приступать к работе.'
    text = \
f'''
Вашу работу {attempt['lesson_title']} проверил преподаватель.
    
Ссылка на работу: {attempt['lesson_url']}
        
{is_right}
'''
    bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    dvmn_token = env.str('DVMN_TOKEN')
    chat_id = env('CHAT_ID')

    bot = telegram.Bot(token=tg_token)

    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    url = 'https://dvmn.org/api/long_polling/'
    params = {}
    while True:
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
