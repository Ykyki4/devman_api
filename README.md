# devman_api
Утилита для взаимодействия с api сайта dvmn.org, при проверке ваших работ, будет отсылаться сообщение от бота чей токен указан в переменной оуркжения, и в чат, указанный в переменной окружения.

## Установка и настройка
Для начала, скачайте репозиторий в .zip или клонируйте его, изолируйте проект с помощью venv и установите зависимости командой:

```
pip install -r requirements.txt
```

Далее, создайте файл .env и установите следующие переменные окружения в формате ПЕРЕМЕННАЯ=значение:

* DVMN_TOKEN - Получить можно по этой [ссылке](https://dvmn.org/api/docs/)
* TG_TOKEN - Зарегистрировать нового бота можно [тут](https://telegram.me/BotFather)
* TG_CHAT_ID - Можно достать при помощи этого [бота](https://telegram.me/userinfobot)
 
После этих шагов, вы можете запускать скрипт командой:

```
python main.py
```

Чтобы проверить, работает ли всё корректно, вы можете отправить работу на проверку, и не дожидаясь проверки от преподавателя, верните работу с проверки.
