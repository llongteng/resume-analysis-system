import sqlite3
import json
from contextlib import contextmanager

_db_path: str | None = None


def get_db_path() -> str:
    """惰性获取数据库路径，首次调用时才读取配置"""
    global _db_path
    if _db_path is None:
        from app.core.config import get_settings
        settings = get_settings()
        # sqlite:///./storage/app.db -> ./storage/app.db
        _db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    return _db_path


@contextmanager
def get_db_connection():
    """获取 SQLite 连接的上下文管理器"""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """初始化数据库表结构"""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_hash TEXT NOT NULL UNIQUE,
                raw_text TEXT,
                cleaned_text TEXT,
                parsed_data TEXT,
                parse_status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_records (
                id TEXT PRIMARY KEY,
                resume_id TEXT NOT NULL,
                job_description TEXT,
                job_analysis TEXT,
                match_result TEXT,
                match_score INTEGER,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (resume_id) REFERENCES resumes(id)
            )
        """)
