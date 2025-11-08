# Incident Management API

API-сервис для учёта инцидентов, поступающих от операторов, систем мониторинга и партнеров.

## Технологии

- Python 3.8+
- FastAPI - веб-фреймворк
- SQLite - база данных
- SQLAlchemy - ORM

## Установка и запуск

1. Клонируйте репозиторий:
   ```
   git clone <repository-url>
   cd incident-management-api
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Запустите сервер:
   ```
   uvicorn main:app --reload --port 8080
   ```

   Сервер будет доступен по адресу: http://localhost:8000

## Эндпоинты

### Создание инцидента

```
POST /incidents/
```

Пример запроса:
```json
{
  "description": "Самокат не в сети",
  "source": "operator"
}
```

### Получение списка инцидентов

```
GET /incidents/
```

С фильтром по статусу:
```
GET /incidents/?status=new
```

Возможные значения статуса: `new`, `in_progress`, `resolved`, `closed`

### Обновление статуса инцидента

```
PATCH /incidents/{incident_id}
```

Пример запроса:
```json
{
  "status": "in_progress"
}
```

## Документация API

После запуска сервера документация будет доступна по адресам:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)