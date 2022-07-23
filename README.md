# VKStars

Баллы за активность в группе вконтакте

## Как это будет выглядеть
Если пользователь находится в топ 10
![Screenshot](docs/1.jpg)
Если пользователь не находится в топ 10
![Screenshot](docs/2.JPG)
Если пользователя нет в базе данных
![Screenshot](docs/3.JPG)
## Использование

Устанавливаем зависимости

`pip install -r requirements.txt`

В файле `data/const.py` настраиваем значения

Запускаем `python get_stats.py` для сбора статистики группы

Запускаем `python app.py` для старта приложения