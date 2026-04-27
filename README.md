# Yatube API

REST API для социальной сети Yatube. Позволяет работать с постами, комментариями, группами и подписками через API интерфейс.

## Возможности Yatube API

- Создание, редактирование и удаление постов
- Комментирование постов
- Добавление постов в группы и управление группами
- Система подписок на авторов
- JWT-аутентификация

## Необходимые приложения

- Python 3.9+
- Django 4.9
- Django REST Framework
- Simple JWT
- SQLite

## Установка и запуск

### 1. Клонирование репозитория и переход в него
```
git clone https://github.com/AndreyAlyazhedinov/api-final-yatube.git
```

```
cd api-final-yatube
```
### 2. Создание виртуального окружения
```
python -m venv venv
```

```
source venv/bin/activate  # Linux/MacOS
# или
source venv/Scripts/activate     # Windows
```
### 3. Установка зависимостей
```
pip install -r requirements.txt
```
### 4. Применение миграций
```
python manage.py migrate
```
### 6. Запуск сервера
```
python manage.py runserver
```
Проект будет доступен по адресу: http://localhost:8000/

## Примеры запросов в Postman

### Аутентификация

1. Получение JWT-токена

Метод: POST

URL: http://localhost:8000/api/v1/jwt/create/

Headers:

    Content-Type: application/json

Body (raw JSON):

    ```
    {
        "username": "ваш_username",
        "password": "ваш_пароль"
    }
    ```

Ответ (200 OK):
    
    ```
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

Ошибка (401 Unauthorized):

    ```
    {
        "detail": "No active account found with the given credentials"
    }
    ```

2. Обновление токена

Метод: POST

URL: http://localhost:8000/api/v1/jwt/refresh/

Headers:

    Content-Type: application/json

Body:

    ```
    {
        "refresh": "ваш_refresh_токен"
    }
    ```

Ответ (200 OK):
    
    ```
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

Ошибка (401 Unauthorized):

    ```
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```

### Посты

1. Получить все посты (без авторизации)

Метод: GET

URL: http://localhost:8000/api/v1/posts/

Ответ (200 OK):

    ```
    {
        "count": 28,
        "next": "http://localhost:8000/api/v1/posts/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "author": "user",
                "text": "Текст первого поста",
                "pub_date": "2025-8-15T12:00:00Z",
                "group": 1,
                "image": null
            },
            {
                "id": 2,
                "author": "anotheruser",
                "text": "Текст второго поста",
                "pub_date": "2025-8-15T11:30:00Z",
                "group": null,
                "image": "/media/posts/image1.jpg"
            }
        ]
    }
    ```

2. Создать новый пост

Метод: POST

URL: http://localhost:8000/api/v1/posts/

Headers:

    Authorization: Bearer ваш_access_токен

    Content-Type: application/json

Body:

    ```
    {
        "text": "Текст поста",
        "group": 1
    }
    ```

Ответ (201 Created):

    ```
    {
        "id": 3,
        "author": "testuser",
        "text": "Текст поста",
        "pub_date": "2025-8-15T14:25:00Z",
        "group": 1,
        "image": null
    }
    ```

Ошибка (400 Bad Request):

    ```
    {
        "text": ["This field is required."]
    }
    ```

3. Обновить пост (только автор)

Метод: PUT

URL: http://localhost:8000/api/v1/posts/1/

Headers:

    Authorization: Bearer ваш_access_токен

    Content-Type: application/json

Body:

    ```
    {
        "text": "Обновленный текст поста",
        "group": null
    }
    ```

Ответ (200 OK):

    ```
    {
        "id": 1,
        "author": "testuser",
        "text": "Обновленный текст поста",
        "pub_date": "2025-8-15T12:00:00Z",
        "group": null,
        "image": null
    }
    ```

Ошибка (403 Forbidden):

    ```
    {
        "detail": "У вас недостаточно прав для выполнения данного действия."
    }
    ```

### Комментарии

1. Получить комментарии к посту

Метод: GET

URL: http://localhost:8000/api/v1/posts/1/comments/

Ответ: (200 OK):

    ```
    [
        {
            "id": 1,
            "author": "user1",
            "text": "Отличная публикация!",
            "created": "2025-8-15T12:05:00Z",
            "post": 1
        },
        {
            "id": 2,
            "author": "user2",
            "text": "Согласен с автором",
            "created": "2025-8-15T12:10:00Z"
            "post": 1
        }
    ]
    ```

2. Добавить комментарий

Метод: POST

URL: http://localhost:8000/api/v1/posts/1/comments/

Headers:

    Authorization: Bearer ваш_access_токен

    Content-Type: application/json

Body:

    ```
    {
        "text": "Текст комментария"
    }
    ```

Ответ (201 Created):

    ```
    {
        "id": 3,
        "author": "testuser",
        "text": "Текст комментария",
        "created": "2025-8-15T14:30:00Z",
        "post": 1
    }
    ```

Ошибка (400 Bad Request):

    ```
    {
        "text": ["This field is required."]
    }
    ```

### Группы

1. Получить список групп

Метод: GET

URL: http://localhost:8000/api/v1/groups/

Ответ (200 OK):

    ```
    [
        {
            "id": 1,
            "title": "Группа 1",
            "slug": "group1",
            "description": "Описание группы 1"
        },
        {
            "id": 2,
            "title": "Группа 2",
            "slug": "group2",
            "description": "Описание группы 2"
        }
    ]
    ```

2. Получить информацию о группе

Метод: GET

URL: http://localhost:8000/api/v1/groups/1/

Ответ (200 OK):

    ```
    {
        "id": 1,
        "title": "Группа 1",
        "slug": "group1",
        "description": "Описание группы 1"
    }
    ```

Ошибка (404 Not Found):

    ```
    {
        "detail": "Страница не найдена."
    }
    ```

### Подписки

1. Получить мои подписки

Метод: GET

URL: http://localhost:8000/api/v1/follow/

Headers:

    Authorization: Bearer ваш_access_токен

Ответ (200 OK):

    ```
    [
        {
            "user": "testuser",
            "following": "author1"
        },
        {
            "user": "testuser",
            "following": "author2"
        }
    ]
    ```

2. Подписаться на пользователя

Метод: POST

URL: http://localhost:8000/api/v1/follow/

Headers:

    Authorization: Bearer ваш_access_токен

    Content-Type: application/json

Body:

    ```
    {
        "following": "username_автора"
    }
    ```

Ответ (201 Created):

    ```
    {
        "user": "testuser",
        "following": "username_автора"
    }
    ```

Ошибка (400 Bad Request):

    ```
    {
        "non_field_errors": ["Вы уже подписаны на этого пользователя"]
    }
    ```

## Документация API
После запуска проекта документация доступна по адресу:

http://localhost:8000/redoc/ - ReDoc документация

## Автор проекта

Аляжединов Андрей
