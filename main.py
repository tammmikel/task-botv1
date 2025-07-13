import json
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from config import BOT_TOKEN
from database.connection import db
from handlers import start

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальные объекты
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключение роутеров
dp.include_router(start.router)

async def handler(event, context):
    """Обработчик Yandex Function"""
    
    # Инициализация БД при первом запуске
    if not db.driver:
        try:
            await db.connect()
            await db.create_tables()
            logger.info("✅ БД инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка БД: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    try:
        # Получаем update из тела запроса
        body = event.get('body', '{}')
        if isinstance(body, str):
            update_data = json.loads(body)
        else:
            update_data = body
        
        # Создаем объект Update
        update = Update(**update_data)
        
        # Обрабатываем update
        await dp.feed_update(bot, update)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }