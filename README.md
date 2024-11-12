# Pet Microservices (DDD, FastAPI, Kafka, MongoDB, Docker)

## Запуск проекта

1. **Клонируйте репозиторий:**
   ```sh
   git clone <URL>
   cd Pet
   ```
2. **Запустите все сервисы и инфраструктуру:**
   ```sh
   docker-compose up --build
   ```
   Это поднимет:
   - orders (порт 8001)
   - logistics (порт 8002)
   - notifications (порт 8003)
   - frontend (порт 3000)
   - Kafka, MongoDB, Zookeeper, nginx

3. **Проверьте доступность сервисов:**
   - http://localhost:8001/docs — OpenAPI orders
   - http://localhost:8002/docs — OpenAPI logistics
   - http://localhost:8003/docs — OpenAPI notifications
   - http://localhost:3000 — фронтенд

---

## DDD-структура сервисов

```
orders/
  domain/
    models.py         # Бизнес-модели
  application/
    commands.py       # Use-cases
  infrastructure/
    db.py             # Работа с MongoDB
    kafka_producer.py # Работа с Kafka
  api/v1/
    endpoints.py      # FastAPI endpoints
  main.py             # Точка входа
  Dockerfile
  pyproject.toml
```

Аналогично для `logistics` и `notifications`.

---

## Документация API

### Orders Service (порт 8001)

#### POST `/orders`
Создать заказ.
- **Тело запроса:**
  ```json
  {
    "user_id": "string",
    "item": "string",
    "quantity": 1
  }
  ```
- **Ответ:**
  ```json
  { "order_id": "string" }
  ```

#### GET `/orders/{order_id}`
Получить заказ по ID.
- **Ответ:**
  ```json
  {
    "_id": "string",
    "user_id": "string",
    "item": "string",
    "quantity": 1
  }
  ```

---

### Logistics Service (порт 8002)

#### POST `/logistics/update`
Обновить статус заказа.
- **Тело запроса:**
  ```json
  {
    "order_id": "string",
    "status": "string"
  }
  ```
- **Ответ:**
  ```json
  { "message": "Status updated" }
  ```

---

### Notifications Service (порт 8003)

#### GET `/notifications/history/{user_id}`
Получить историю уведомлений пользователя.
- **Ответ:**
  ```json
  [
    {
      "_id": "string",
      "user_id": "string",
      "order_id": "string",
      "status": "string"
    }
  ]
  ```

#### WebSocket `/ws/notifications`
Получать уведомления в реальном времени.
- **Подключение:**
  - ws://localhost:8003/ws/notifications
- **События:**
  - При изменении статуса заказа пользователю отправляется уведомление в формате JSON.

---

## Пример сценария

1. Создать заказ через `/orders`.
2. Обновить статус через `/logistics/update`.
3. Получить уведомление через WebSocket или историю через `/notifications/history/{user_id}`.

---

## Требования
- Docker, Docker Compose
- (Локально) Python 3.11+, Poetry (если запускать вне Docker)

---

## Авторы
- AwakeGit
