# Боты способные вести диалог в Телеграме и личных сообщения Вконтакте
Боты модуг отвечать на вопросы пользователей. В качестве ML движка используется Dialogflow от гугла.

![Телеграм бот](tg_demo.gif)

### Предварительная подготовка
Для работы ботов нужно будет создать проект на платформе Google Cloud Platform и зарегистрировать сервисный ключ. При
выпуске ключа нужно выбрать `JSON` формат. После скачивания файла, уго можно положить в папку с программой или иное место
и указать путь к файлу в переменной окружения `GOOGLE_APPLICATION_CREDENTIALS` Пошаговая инструкция 
на [этой странице](https://cloud.google.com/dialogflow/docs/quickstart-api) в разделе
"Set up your GCP project and authentication"

Кроме того, нужно будет создать агента в консоли Dialogflow. Пошаговая инструкция
[на этой странице](https://cloud.google.com/dialogflow/docs/quickstart-api) в разделе "Create an agent". После создания
агента, нужно будет зайти в его настройки, найти идентификатор проекта и записать в переменную окружения
`DIALOGFLOW_PROJECT_ID`

### Как установить
Для работы скрипта нужно зарегистрировать в операционной системе переменные окружения

- `TG_TOKEN` - Токен бота в телеграме
- `TG_CHAT_ID` - @Идентификатор телеграмм-чата или пользователя куда будут приходить сообщения об ошибках
(например @smmreposting)

- `VK_GROUP_TOKEN` - токен доступа к группе Вконтакте. При регистрации нужно будет дать права работу с сообщениями.

- `GOOGLE_APPLICATION_CREDENTIALS` - путь к json файлу с ключами к google.cloud 
- `DIALOGFLOW_PROJECT_ID` - идентификатор проекта в Dialogflow
 
- `QUESTIONS_FILE` - Путь к json файлу с вопросами и ответами для обучения ботов 

- `LOG_LEVEL` - уровень логирования (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL). Подробно о каждом уровне
описано [тут](https://docs.python.org/3/library/logging.html)

 
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как использовать
Боты запускаются по отдельности. Для каждого бота свой процесс. Для запуска бота нужно запустить `main.py` с ключем
`-startbot`. После ключа нужно передать одно из значений `tg` для запуска телеграм-бота или `vk` для запуска бота
вконтакте

Пример использования
```sh
python main.py -startbot vk
```

```sh
python main.py -startbot tg
```

### Как обучать
Для обучения ботов нужно подготовить json файл в котором будут находится учебные сеты. Пример содержимого такого файла
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Хочу работать с вами",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа."
    }
}
```

Путь к файлу нужно прописать в переменную окружения `QUESTIONS_FILE`

После подготовки файла нужно запустить программу с ключем `-train`. Так же, можно использовать опциональный ключ
`--forse` который заставляет программу заменять ответы в Dialogflow на ответы из файла при повторном переобучении.

Пример использования
```sh
python main.py -train
```

```sh
python main.py -train --forse
```

### Деплой и запуск на Heroku
Бота можно запустить на [Heroku](https://.heroku.com). Нужно создать на Heroku новое приложение, связать его с
репозиторием, задеплоить и сбилдить исходники.

В настройках приложения на heroku (вкладка Settings) нужно добавить в Config Vars переменные окружения и их значения
описанные в разделе Как установить. Чтобы не забивать логи инстанса на heroku, `LOG_LEVEL` лучше выставить значение
`INFO`
О том как добавить ключи от Google написано [здесь](https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku)

После настройки приложение нужно запустить во вкладке `Resource`. Если скрипт запустится корректно, телеграм-бот пришлет
сообщения о запуске ботов вида
```
2019-07-19 10:46:04,236
vk_bot
INFO
VK bot started
```

Если произойдет ошибка бот напишет в телеграм сообщение вида
```
2019-07-19 10:46:05,297
vk_bot
ERROR
[5] User authorization failed: invalid access_token (4).
```

Для управления ботом на Heroku из коммандной строки нужно установить
[heroku cli](https://devcenter.heroku.com/categories/command-line) и авторизоваться из терминала в Heroku

Для проверки статуса приложения из терминала нужно выполнить команду
```sh
heroku ps -a название_приложения_на_heroku
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.