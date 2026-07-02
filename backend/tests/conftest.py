import os
import pytest
from fastapi.testclient import TestClient

# 设置测试环境变量（必须在 import app 之前）
os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("DATABASE_URL", "sqlite:///./storage/test.db")
os.environ.setdefault("CACHE_ENABLED", "false")
os.environ.setdefault("AI_API_KEY", "test_key")

from app.main import app
from app.models.database import init_db, get_db_connection


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """测试前初始化数据库，测试后清理"""
    init_db()
    yield
    # 清理测试数据库
    try:
        os.remove("./storage/test.db")
    except FileNotFoundError:
        pass


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture
def test_pdf_path():
    """创建测试 PDF 文件"""
    import fitz

    path = "./storage/uploads/test_resume.pdf"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "张三\n13800000000\nzhangsan@test.com\n杭州\nPython FastAPI MySQL Redis")
    doc.save(path)
    doc.close()

    yield path

    # 清理
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
