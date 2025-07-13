from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.queries import UserQueries
from config import ROLES

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    """Обработка команды /start"""
    user = message.from_user
    
    # Проверяем, есть ли пользователь в БД
    existing_user = await UserQueries.get_user(user.id)
    
    if existing_user:
        role_name = ROLES.get(existing_user['role'], existing_user['role'])
        await message.reply(
            f"👋 Привет, {user.first_name}!\n"
            f"Ваша роль: {role_name}\n\n"
            f"Доступные команды:\n"
            f"/menu - Главное меню\n"
            f"/tasks - Мои задачи"
        )
        return
    
    # Определяем роль для нового пользователя
    users_count = await UserQueries.get_users_count()
    role = 'DIRECTOR' if users_count == 0 else 'SYS_ADMIN'
    
    # Создаем пользователя
    await UserQueries.create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role
    )
    
    role_name = ROLES.get(role, role)
    
    welcome_msg = f"🎉 Добро пожаловать, {user.first_name}!\n"
    welcome_msg += f"Ваша роль: {role_name}\n\n"
    
    if role == 'DIRECTOR':
        welcome_msg += "🎯 Вы первый пользователь - получили роль Директора\n"
        welcome_msg += "Вы можете:\n"
        welcome_msg += "• Создавать компании и задачи\n"
        welcome_msg += "• Назначать роли сотрудникам\n"
        welcome_msg += "• Смотреть аналитику\n\n"
    else:
        welcome_msg += "👤 Вы получили роль Системного админа\n"
        welcome_msg += "Директор может изменить вашу роль при необходимости\n\n"
    
    welcome_msg += "Команды:\n"
    welcome_msg += "/menu - Главное меню\n"
    welcome_msg += "/tasks - Мои задачи"
    
    await message.reply(welcome_msg)

@router.message(Command('menu'))
async def menu_handler(message: Message):
    """Главное меню"""
    user = await UserQueries.get_user(message.from_user.id)
    
    if not user:
        await message.reply("❌ Пользователь не найден. Используйте /start")
        return
    
    role = user['role']
    menu_text = "📋 Главное меню\n\n"
    
    if role in ['DIRECTOR', 'MANAGER']:
        menu_text += "🏢 /companies - Управление компаниями\n"
        menu_text += "➕ /new_task - Создать задачу\n"
    
    if role == 'DIRECTOR':
        menu_text += "👥 /users - Управление пользователями\n"
        menu_text += "📊 /analytics - Аналитика\n"
    
    menu_text += "📝 /tasks - Мои задачи\n"
    menu_text += "ℹ️ /info - Информация о боте"
    
    await message.reply(menu_text)

@router.message(Command('info'))
async def info_handler(message: Message):
    """Информация о боте"""
    user = await UserQueries.get_user(message.from_user.id)
    
    if not user:
        await message.reply("❌ Используйте /start для регистрации")
        return
    
    role_name = ROLES.get(user['role'], user['role'])
    
    info_text = f"ℹ️ Информация о боте\n\n"
    info_text += f"👤 Пользователь: {user['first_name']}\n"
    info_text += f"🎭 Роль: {role_name}\n\n"
    info_text += f"📋 Бот для управления задачами\n"
    info_text += f"🏢 Компания аутсорсинга\n\n"
    info_text += f"💡 Для помощи обращайтесь к директору"
    
    await message.reply(info_text)