import time
from database.connection import db

class SimpleStates:
    """Простое управление состояниями через YDB"""
    
    @staticmethod
    async def set_state(user_id, state, data=None):
        """Установить состояние пользователя"""
        query = """
        UPSERT INTO user_states (user_id, state, data, created_at)
        VALUES ($user_id, $state, $data, $created_at)
        """
        params = {
            '$user_id': user_id,
            '$state': state,
            '$data': data or '{}',
            '$created_at': int(time.time() * 1000000)
        }
        await db.execute_query(query, params)
    
    @staticmethod
    async def get_state(user_id):
        """Получить состояние пользователя"""
        query = "SELECT state, data FROM user_states WHERE user_id = $user_id"
        result = await db.execute_query(query, {'$user_id': user_id})
        return result[0].rows[0] if result[0].rows else None
    
    @staticmethod
    async def clear_state(user_id):
        """Очистить состояние"""
        query = "DELETE FROM user_states WHERE user_id = $user_id"
        await db.execute_query(query, {'$user_id': user_id})

# Создание таблицы состояний
CREATE_STATES_TABLE = """
CREATE TABLE user_states (
    user_id Int64 NOT NULL,
    state String NOT NULL,
    data String,
    created_at Timestamp NOT NULL,
    PRIMARY KEY (user_id)
)
"""