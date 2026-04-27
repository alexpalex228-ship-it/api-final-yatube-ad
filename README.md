# API для Yatube

## Описание
Проект Yatube API предоставляет программный интерфейс для социальной сети блогеров Yatube. Сервис позволяет взаимодействовать с контентом платформы через RESTful API: публиковать посты, оставлять комментарии, просматривать тематические группы и подписываться на интересных авторов.

Аутентификация в проекте реализована с помощью JWT-токенов. Неавторизованные пользователи имеют доступ к API только в режиме чтения (кроме эндпоинта подписок).

## Технологии
- Python 3.10
- Django 3.2.16
- Django REST Framework 3.12.4
- SimpleJWT (Аутентификация)
- SQLite3

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your_username/api_final_yatube.git
```

2. Cоздайте и активируйте виртуальное окружение:
```bash
python3.10 -m venv venv
source venv/bin/activate  # Для Linux/macOS
source venv/Scripts/activate  # Для Windows
```

3. Установите зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```

4. Выполните миграции:
```bash
python manage.py migrate
```

5. Запустите проект:
```bash
python manage.py runserver
```

## Примеры запросов к API

### Регистрация/Получение токена (POST)
`http://127.0.0.1:8000/api/v1/jwt/create/`
Передайте `username` и `password`. В ответ придут `access` и `refresh` токены.

### Получение списка всех постов (GET)
`http://127.0.0.1:8000/api/v1/posts/`

### Создание нового поста (POST)
`http://127.0.0.1:8000/api/v1/posts/`
В заголовке запроса передайте: `Authorization: Bearer <ваш_токен>`
```json
{
    "text": "Текст нового поста",
    "group": 1
}
```

### Подписка на автора (POST)
`http://127.0.0.1:8000/api/v1/follow/`
```json
{
    "following": "username_автора"
}
```
