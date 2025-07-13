from database.connection import db
from datetime import datetime
import time

class UserQueries:
    
    @staticmethod
    async def create_user(user_id, username, first_name, last_name, role):
        """Создание пользователя"""
        query = """
        UPSERT INTO users (user_id, username, first_name, last_name, role, created_at)
        VALUES ($user_id, $username, $first_name, $last_name, $role, $created_at)
        """
        params = {
            '$user_id': user_id,
            '$username': username,
            '$first_name': first_name,
            '$last_name': last_name,
            '$role': role,
            '$created_at': int(time.time() * 1000000)  # микросекунды
        }
        await db.execute_query(query, params)
    
    @staticmethod
    async def get_user(user_id):
        """Получение пользователя"""
        query = "SELECT * FROM users WHERE user_id = $user_id"
        result = await db.execute_query(query, {'$user_id': user_id})
        return result[0].rows[0] if result[0].rows else None
    
    @staticmethod
    async def get_users_count():
        """Количество пользователей"""
        query = "SELECT COUNT(*) as count FROM users"
        result = await db.execute_query(query)
        return result[0].rows[0]['count']
    
    @staticmethod
    async def get_users_by_role(role):
        """Пользователи по роли"""
        query = "SELECT * FROM users WHERE role = $role"
        result = await db.execute_query(query, {'$role': role})
        return result[0].rows
    
    @staticmethod
    async def update_user_role(user_id, role):
        """Изменение роли"""
        query = "UPDATE users SET role = $role WHERE user_id = $user_id"
        await db.execute_query(query, {'$user_id': user_id, '$role': role})

class CompanyQueries:
    
    @staticmethod
    async def create_company(company_id, name, description, created_by):
        """Создание компании"""
        query = """
        INSERT INTO companies (company_id, name, description, created_by, created_at)
        VALUES ($company_id, $name, $description, $created_by, $created_at)
        """
        params = {
            '$company_id': company_id,
            '$name': name,
            '$description': description,
            '$created_by': created_by,
            '$created_at': int(time.time() * 1000000)
        }
        await db.execute_query(query, params)
    
    @staticmethod
    async def get_companies():
        """Все компании"""
        query = "SELECT * FROM companies ORDER BY created_at DESC"
        result = await db.execute_query(query)
        return result[0].rows

class TaskQueries:
    
    @staticmethod
    async def create_task(task_id, title, description, company_id, initiator, 
                         initiator_phone, assignee_id, created_by, priority, 
                         status, deadline):
        """Создание задачи"""
        query = """
        INSERT INTO tasks (task_id, title, description, company_id, initiator, 
                          initiator_phone, assignee_id, created_by, priority, 
                          status, deadline, created_at)
        VALUES ($task_id, $title, $description, $company_id, $initiator, 
                $initiator_phone, $assignee_id, $created_by, $priority, 
                $status, $deadline, $created_at)
        """
        params = {
            '$task_id': task_id,
            '$title': title,
            '$description': description,
            '$company_id': company_id,
            '$initiator': initiator,
            '$initiator_phone': initiator_phone,
            '$assignee_id': assignee_id,
            '$created_by': created_by,
            '$priority': priority,
            '$status': status,
            '$deadline': deadline,
            '$created_at': int(time.time() * 1000000)
        }
        await db.execute_query(query, params)
    
    @staticmethod
    async def get_task(task_id):
        """Получение задачи"""
        query = "SELECT * FROM tasks WHERE task_id = $task_id"
        result = await db.execute_query(query, {'$task_id': task_id})
        return result[0].rows[0] if result[0].rows else None
    
    @staticmethod
    async def update_task_status(task_id, status, completed_at=None):
        """Изменение статуса задачи"""
        if completed_at:
            query = """
            UPDATE tasks SET status = $status, completed_at = $completed_at 
            WHERE task_id = $task_id
            """
            params = {
                '$task_id': task_id,
                '$status': status,
                '$completed_at': completed_at
            }
        else:
            query = "UPDATE tasks SET status = $status WHERE task_id = $task_id"
            params = {'$task_id': task_id, '$status': status}
        
        await db.execute_query(query, params)
    
    @staticmethod
    async def get_tasks_by_assignee(assignee_id):
        """Задачи по исполнителю"""
        query = "SELECT * FROM tasks WHERE assignee_id = $assignee_id ORDER BY created_at DESC"
        result = await db.execute_query(query, {'$assignee_id': assignee_id})
        return result[0].rows