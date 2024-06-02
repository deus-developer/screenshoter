# Screenshot Service

Это маленький сервис для создания скриншотов, который можно поднять с помощью Docker Compose.

## Содержание

- [Содержание](#содержание)
- [Требования](#требования)
- [Установка](#установка)
- [Использование](#использование)
- [API документация](#api-документация)
  - [Создать контекст](#создать-контекст)
  - [Получить все контексты](#получить-все-контексты)
  - [Получить контекст](#получить-контекст)
  - [Изменить контекст](#изменить-контекст)
  - [Сделать скриншот](#сделать-скриншот)
- [Конфигурация](#конфигурация)
- [Структура проекта](#структура-проекта)
- [Лицензия](#лицензия)

## Требования

- Docker
- Docker Compose

## Установка

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/deus-developer/screenshoter.git
    cd screenshoter
    ```

2. Поднимите сервисы с помощью Docker Compose:

    ```bash
    docker-compose up -d
    ```

## Использование

После того как сервис будет запущен, он станет доступен на локальном хосте по адресу `http://127.0.0.1:8080`.

Вы можете отправлять HTTP запросы к этому сервису для создания скриншотов.

## API документация

### Создать контекст

Создает новый контекст для браузера.

- **URL**: `/settings`
- **Метод**: `POST`
- **Тело запроса**:

```json
{
  "name": "UUID контекста",
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "geolocation": {
    "latitude": 55.7558,
    "longitude": 37.6176
  },
  "ignore_https_errors": true,
  "java_script_enabled": true,
  "user_agent": "строка user-agent",
  "locale": "ru-RU",
  "timezone": "Europe/Moscow",
  "device_scale_factor": 1.0,
  "is_mobile": false,
  "has_touch": false,
  "color_scheme": "light",
  "accept_downloads": true,
  "service_workers": "allow",
  "bypass_csp": true,
  "permissions": ["geolocation", "notifications"]
}
```

- **Ответ**:

  - **200 OK**: `true`
  - **422 Unprocessable Entity**: Ошибка валидации

### Получить все контексты

Возвращает список всех созданных контекстов.

- **URL**: `/settings/list`
- **Метод**: `GET`
- **Ответ**:

  - **200 OK**: Список объектов `BrowserSettings`

### Получить контекст

Возвращает информацию о контексте по его имени (UUID).

- **URL**: `/settings/{name}`
- **Метод**: `GET`
- **Параметры**:

  - `name`: UUID контекста (строка)

- **Ответ**:

  - **200 OK**: Объект `BrowserSettings`
  - **422 Unprocessable Entity**: Ошибка валидации

### Изменить контекст

Изменяет существующий контекст по его имени (UUID).

- **URL**: `/settings/{name}`
- **Метод**: `PATCH`
- **Параметры**:

  - `name`: UUID контекста (строка)

- **Тело запроса**:

```json
{
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "geolocation": {
    "latitude": 55.7558,
    "longitude": 37.6176
  },
  "ignore_https_errors": true,
  "java_script_enabled": true,
  "user_agent": "строка user-agent",
  "locale": "ru-RU",
  "timezone": "Europe/Moscow",
  "device_scale_factor": 1.0,
  "is_mobile": false,
  "has_touch": false,
  "color_scheme": "light",
  "accept_downloads": true,
  "service_workers": "allow",
  "bypass_csp": true,
  "permissions": ["geolocation", "notifications"]
}
```

- **Ответ**:

  - **200 OK**: `true`
  - **422 Unprocessable Entity**: Ошибка валидации

### Сделать скриншот

Создает скриншот страницы по заданному URL.

- **URL**: `/screenshot`
- **Метод**: `POST`
- **Параметры**:

  - `name`: UUID контекста (строка, query параметр)

- **Тело запроса**:

```json
{
  "url": "https://example.com",
  "referer": "https://referer.com",
  "omit_background": false,
  "full_page": false,
  "clip_settings": {
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 1080
  },
  "animations": "allow",
  "timeout": 60,
  "wait": 0
}
```

- **Ответ**:

  - **200 OK**: Успешный ответ
  - **422 Unprocessable Entity**: Ошибка валидации

## Конфигурация

В файле `docker-compose.yml` определены следующие сервисы:

- **mongo**: база данных MongoDB для хранения данных.
- **screenshot-service**: сервис для создания скриншотов.

### Параметры среды для screenshot-service

- `MONGODB_DSN`: строка подключения к MongoDB. По умолчанию `mongodb://mongo-server:27017/`.
- `MONGODB_DATABASE_NAME`: имя базы данных MongoDB. По умолчанию `screenshoter`.
- `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD`: переменная окружения для Playwright, чтобы пропустить скачивание браузеров. Значение `1`.

## Структура проекта

- `docker-compose.yml`: файл конфигурации для Docker Compose.
- `volumes/`: директория для хранения данных MongoDB и контекстов браузера.
- `src/`: исходный код сервиса.

## Лицензия

Этот проект лицензируется под лицензией MIT. Подробности можно найти в файле `LICENSE`.
