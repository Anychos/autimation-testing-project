# Автоматизация тестирования TaskFlow

Учебный проект для практики автоматизации тестирования приложения [TaskFlow](https://github.com/Anychos/autimation-testing-project-app). Сейчас в проекте реализованы API-тесты. UI-тесты планируются, но пока не написаны.

## Что проверяется

- Регистрация и вход: успешные сценарии, некорректные данные, повторная регистрация и ошибки входа.
- Задачи: создание, получение одной задачи и списка, изменение и удаление.
- Граничные значения названия задачи и некорректные параметры списка.
- Изоляция данных: другой пользователь не видит задачу и не может её прочитать или удалить.

Ответы проверяются с помощью Pydantic-схем и переиспользуемых проверок. Для авторизованных запросов клиент использует cookies и CSRF-токен.

## Инструменты

- **Python и pytest** — написание и запуск тестов.
- **HTTPX** — работа с API.
- **Pydantic** — схемы запросов, ответов и настроек.
- **Faker** — генерация тестовых данных.
- **Ruff** — проверка качества кода.
- **Playwright** — зависимость для будущих UI-тестов.
- **Docker Compose** — запуск приложения и базы данных для тестирования.

## Подготовка к запуску

Понадобятся Python 3.12, Docker и Docker Compose. Скачайте [репозиторий приложения](https://github.com/Anychos/autimation-testing-project-app), затем в его папке выполните:

```powershell
Copy-Item .env.example .env
# Укажите локальный POSTGRES_PASSWORD в .env приложения.
docker compose up -d --build --wait backend
```

В корне этого репозитория создайте виртуальное окружение, установите зависимости и подготовьте настройки тестов:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

В `.env` тестового проекта по умолчанию указаны адрес API `http://localhost:8000` и таймаут 10 секунд. При необходимости измените `HTTP_CLIENT.BASE_URL` и `HTTP_CLIENT.TIMEOUT`.

## Запуск тестов

Команды выполняются из корня тестового проекта при запущенном backend:

```powershell
# Все тесты
.\.venv\Scripts\python.exe -m pytest

# Smoke- и регрессионные тесты
.\.venv\Scripts\python.exe -m pytest -m smoke
.\.venv\Scripts\python.exe -m pytest -m regression

# Отдельные модули
.\.venv\Scripts\python.exe -m pytest tests/api/test_auth.py
.\.venv\Scripts\python.exe -m pytest tests/api/test_tasks.py
```

Тесты и фикстуры регистрируют пользователей. Созданные через фикстуры задачи и задачи, ID которых зарегистрирован для очистки, удаляются после тестов; если тест уже удалил задачу, очистка учитывает ответ `TASK_NOT_FOUND`. Пользователи автоматически не удаляются, поэтому используйте тестовое окружение.

## Smoke-тесты в GitHub Actions

При каждом push workflow получает репозиторий приложения, запускает backend с PostgreSQL через Docker Compose и выполняет тесты с маркером `smoke`. После запуска контейнеры и их тома удаляются; при ошибке в журнал выводятся логи приложения. Результат доступен во вкладке Actions репозитория тестов.

## Структура проекта

```text
.github/workflows/  Запуск smoke-тестов в GitHub Actions
src/api/assertions/ Переиспользуемые проверки ответов API
src/api/clients/    API-клиенты и создание HTTP-клиентов
src/api/fixtures/   Подготовка пользователей, клиентов и задач, очистка задач
src/api/schemas/    Pydantic-схемы запросов и ответов
src/api/tools/      Маршруты API и генерация данных
src/api/config.py   Загрузка настроек API
src/ui/             Страницы и компоненты пользовательского интерфейса
tests/api/          API-тесты авторизации и задач
.env.example        Пример настроек тестового проекта
conftest.py         Подключение общих фикстур pytest
pytest.ini          Настройки и маркеры pytest
requirements.txt    Зависимости проекта
```
