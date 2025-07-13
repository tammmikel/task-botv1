import ydb
import asyncio
from config import YDB_ENDPOINT, YDB_DATABASE, YDB_TOKEN
from database.models import CREATE_TABLES

class Database:
    def __init__(self):
        self.driver = None
        self.pool = None
    
    async def connect(self):
        """Подключение к YDB"""
        try:
            self.driver = ydb.Driver(
                endpoint=YDB_ENDPOINT,
                database=YDB_DATABASE,
                credentials=ydb.AccessTokenCredentials(YDB_TOKEN)
            )
            
            await asyncio.get_event_loop().run_in_executor(
                None, self.driver.wait, 30
            )
            
            self.pool = ydb.SessionPool(self.driver)
            print("✅ YDB подключена")
            
        except Exception as e:
            print(f"❌ Ошибка подключения к YDB: {e}")
            raise
    
    async def create_tables(self):
        """Создание таблиц"""
        def _create_tables(session):
            for table_sql in CREATE_TABLES:
                try:
                    session.execute_scheme(table_sql)
                except Exception as e:
                    if "already exists" not in str(e):
                        raise
        
        await asyncio.get_event_loop().run_in_executor(
            None, self.pool.retry_operation_sync, _create_tables
        )
        print("✅ Таблицы созданы")
    
    async def execute_query(self, query, parameters=None):
        """Выполнение запроса"""
        def _execute(session):
            prepared = session.prepare(query)
            return session.transaction().execute(
                prepared, parameters or {}, commit_tx=True
            )
        
        return await asyncio.get_event_loop().run_in_executor(
            None, self.pool.retry_operation_sync, _execute
        )
    
    async def close(self):
        """Закрытие соединения"""
        if self.driver:
            self.driver.stop()

# Глобальный экземпляр
db = Database()