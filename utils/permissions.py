from database.queries import UserQueries

class Permissions:
    
    @staticmethod
    async def check_user_role(user_id, required_roles):
        """Проверка роли пользователя"""
        user = await UserQueries.get_user(user_id)
        if not user:
            return False
        
        if isinstance(required_roles, str):
            required_roles = [required_roles]
        
        return user['role'] in required_roles
    
    @staticmethod
    async def can_create_tasks(user_id):
        """Может ли создавать задачи"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR', 'MANAGER'])
    
    @staticmethod
    async def can_create_companies(user_id):
        """Может ли создавать компании"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR', 'MANAGER'])
    
    @staticmethod
    async def can_change_roles(user_id):
        """Может ли менять роли"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR'])
    
    @staticmethod
    async def can_view_analytics(user_id):
        """Может ли смотреть аналитику"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR'])
    
    @staticmethod
    async def can_change_task_status(user_id):
        """Может ли менять статус задачи"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR', 'MANAGER', 'MAIN_ADMIN', 'SYS_ADMIN'])
    
    @staticmethod
    async def can_reopen_task(user_id):
        """Может ли переоткрыть задачу"""
        return await Permissions.check_user_role(user_id, ['DIRECTOR', 'MANAGER'])

def require_permission(permission_func):
    """Декоратор для проверки прав"""
    def decorator(handler):
        async def wrapper(message, *args, **kwargs):
            if not await permission_func(message.from_user.id):
                await message.reply("❌ У вас нет прав для этого действия")
                return
            return await handler(message, *args, **kwargs)
        return wrapper
    return decorator