import os
#from dotenv import load_dotenv

#load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv('BOT_TOKEN')

# YDB
YDB_ENDPOINT = os.getenv('YDB_ENDPOINT')
YDB_DATABASE = os.getenv('YDB_DATABASE')
YDB_TOKEN = os.getenv('YDB_TOKEN')

# Yandex Object Storage
#S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'https://storage.yandexcloud.net')
#S3_BUCKET = os.getenv('S3_BUCKET', 'task-files-bucket')
#S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
#S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')

# Timezone
TIMEZONE = 'Asia/Yekaterinburg'  # UTC+5

# File limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# Roles
ROLES = {
    'DIRECTOR': 'Директор',
    'MANAGER': 'Менеджер', 
    'MAIN_ADMIN': 'Главный админ',
    'SYS_ADMIN': 'Системный админ'
}

# Task statuses
TASK_STATUS = {
    'CREATED': 'Создана',
    'IN_PROGRESS': 'В работе',
    'COMPLETED': 'Выполнена'
}

# Priorities
PRIORITIES = {
    'HIGH': 'Срочная',
    'MEDIUM': 'Нормальная',
    'LOW': 'Не очень срочная'
}