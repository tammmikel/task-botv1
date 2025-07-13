# Простые SQL запросы для создания таблиц

CREATE_TABLES = [
    """
    CREATE TABLE users (
        user_id Int64 NOT NULL,
        username String,
        first_name String,
        last_name String,
        role String NOT NULL,
        created_at Timestamp NOT NULL,
        PRIMARY KEY (user_id)
    )
    """,
    
    """
    CREATE TABLE user_states (
        user_id Int64 NOT NULL,
        state String NOT NULL,
        data String,
        created_at Timestamp NOT NULL,
        PRIMARY KEY (user_id)
    )
    """,
    
    """
    CREATE TABLE companies (
        company_id Int64 NOT NULL,
        name String NOT NULL,
        description String,
        created_by Int64 NOT NULL,
        created_at Timestamp NOT NULL,
        PRIMARY KEY (company_id)
    )
    """,
    
    """
    CREATE TABLE tasks (
        task_id Int64 NOT NULL,
        title String NOT NULL,
        description String,
        company_id Int64 NOT NULL,
        initiator String NOT NULL,
        initiator_phone String NOT NULL,
        assignee_id Int64 NOT NULL,
        created_by Int64 NOT NULL,
        priority String NOT NULL,
        status String NOT NULL,
        deadline Timestamp NOT NULL,
        created_at Timestamp NOT NULL,
        completed_at Timestamp,
        PRIMARY KEY (task_id)
    )
    """,
    
    """
    CREATE TABLE task_comments (
        comment_id Int64 NOT NULL,
        task_id Int64 NOT NULL,
        user_id Int64 NOT NULL,
        message String NOT NULL,
        created_at Timestamp NOT NULL,
        PRIMARY KEY (comment_id)
    )
    """,
    
    """
    CREATE TABLE task_files (
        file_id Int64 NOT NULL,
        task_id Int64 NOT NULL,
        file_name String NOT NULL,
        file_size Int64 NOT NULL,
        file_type String NOT NULL,
        s3_key String NOT NULL,
        uploaded_by Int64 NOT NULL,
        uploaded_at Timestamp NOT NULL,
        PRIMARY KEY (file_id)
    )
    """
]