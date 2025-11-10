from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Сервис уведомлений", description="Сервис для отправки уведомлений через несколько каналов")

# Модели Pydantic
class NotificationRequest(BaseModel):
    user_id: str
    message: str
    channels: List[str]  # email, sms, telegram
    email: Optional[str] = None
    phone: Optional[str] = None
    telegram_id: Optional[str] = None

class NotificationResponse(BaseModel):
    success: bool
    message: str
    channel_used: str

# Мок сервиса SMS
def send_sms(phone: str, message: str) -> bool:
    """Функция отправки SMS (мок)"""
    logger.info(f"Отправка SMS на {phone}: {message}")
    # В реальной реализации здесь будет интеграция с API провайдера SMS
    # Пока симулируем успешную отправку
    return True  # Симуляция успешной отправки

# Функция отправки email
def send_email(email: str, message: str) -> bool:
    """Функция отправки email (мок)"""
    logger.info(f"Отправка email на {email}: {message}")
    # В реальной реализации здесь будут использоваться настоящие настройки SMTP
    # Пока симулируем успешную отправку
    return True  # Симуляция успешной отправки

# Мок сервиса Telegram
def send_telegram(telegram_id: str, message: str) -> bool:
    """Функция отправки сообщения в Telegram (мок)"""
    logger.info(f"Отправка сообщения в Telegram {telegram_id}: {message}")
    # В реальной реализации здесь будет интеграция с Telegram Bot API
    # Пока симулируем успешную отправку
    return True  # Симуляция успешной отправки

# Порядок приоритета каналов
CHANNEL_PRIORITY = ["email", "sms", "telegram"]

@app.post("/notify/", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest):
    """
    Отправка уведомления через доступные каналы с механизмом резервирования.
    Если один канал не работает, пробуем следующий в порядке приоритета.
    """
    if not request.channels:
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы один канал")
    
    # Проверка обязательных полей для указанных каналов
    for channel in request.channels:
        if channel == "email" and not request.email:
            raise HTTPException(status_code=400, detail="Требуется адрес email для email-уведомлений")
        elif channel == "sms" and not request.phone:
            raise HTTPException(status_code=400, detail="Требуется номер телефона для SMS-уведомлений")
        elif channel == "telegram" and not request.telegram_id:
            raise HTTPException(status_code=400, detail="Требуется ID Telegram для Telegram-уведомлений")
    
    # Пробуем каналы в порядке приоритета
    for channel in CHANNEL_PRIORITY:
        if channel in request.channels:
            success = False
            try:
                if channel == "email" and request.email:
                    success = send_email(request.email, request.message)
                elif channel == "sms" and request.phone:
                    success = send_sms(request.phone, request.message)
                elif channel == "telegram" and request.telegram_id:
                    success = send_telegram(request.telegram_id, request.message)
                
                if success:
                    return NotificationResponse(
                        success=True,
                        message=f"Уведомление успешно отправлено через {channel}",
                        channel_used=channel
                    )
            except Exception as e:
                logger.error(f"Не удалось отправить уведомление через {channel}: {str(e)}")
                continue  # Пробуем следующий канал
    
    # Если мы дошли до этой точки, значит все каналы не сработали
    raise HTTPException(status_code=500, detail="Не удалось отправить уведомление ни через один канал")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)