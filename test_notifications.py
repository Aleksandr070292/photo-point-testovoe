import requests
import json

# Тестирование сервиса уведомлений

# Базовый URL
BASE_URL = "http://localhost:8080"

# Тест 1: Отправка email-уведомления
print("Тест 1: Отправка email-уведомления")
response = requests.post(f"{BASE_URL}/notify/", json={
    "user_id": "123",
    "message": "Привет через email!",
    "channels": ["email"],
    "email": "user@example.com"
})
print(f"Ответ: {response.status_code} - {response.json()}")

print("\n" + "="*50 + "\n")

# Тест 2: Отправка SMS-уведомления
print("Тест 2: Отправка SMS-уведомления")
response = requests.post(f"{BASE_URL}/notify/", json={
    "user_id": "456",
    "message": "Привет через SMS!",
    "channels": ["sms"],
    "phone": "+1234567890"
})
print(f"Ответ: {response.status_code} - {response.json()}")

print("\n" + "="*50 + "\n")

# Тест 3: Отправка Telegram-уведомления
print("Тест 3: Отправка Telegram-уведомления")
response = requests.post(f"{BASE_URL}/notify/", json={
    "user_id": "789",
    "message": "Привет через Telegram!",
    "channels": ["telegram"],
    "telegram_id": "@username"
})
print(f"Ответ: {response.status_code} - {response.json()}")

print("\n" + "="*50 + "\n")

# Тест 4: Отправка уведомления с несколькими каналами (механизм резервирования)
print("Тест 4: Отправка уведомления с механизмом резервирования")
response = requests.post(f"{BASE_URL}/notify/", json={
    "user_id": "101",
    "message": "Привет с резервированием!",
    "channels": ["email", "sms", "telegram"],
    "email": "user@example.com",
    "phone": "+1234567890",
    "telegram_id": "@username"
})
print(f"Ответ: {response.status_code} - {response.json()}")

print("\n" + "="*50 + "\n")

# Тест 5: Проверка работоспособности
print("Тест 5: Проверка работоспособности")
response = requests.get(f"{BASE_URL}/health")
print(f"Ответ: {response.status_code} - {response.json()}")