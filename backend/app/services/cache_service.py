import json
import hashlib

import redis

from app.core.config import get_settings
from app.core.logging import logger

_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis | None:
    """获取 Redis 客户端（懒加载）"""
    global _redis_client
    settings = get_settings()

    if not settings.CACHE_ENABLED:
        return None

    if _redis_client is None:
        try:
            _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            _redis_client.ping()
            logger.info("Redis 连接成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败，降级为无缓存模式: {e}")
            _redis_client = None

    return _redis_client


def compute_hash(text: str) -> str:
    """计算文本的 MD5 哈希（用于缓存 key）"""
    return hashlib.md5(text.encode()).hexdigest()


def get_cached(key: str) -> dict | None:
    """从缓存获取数据"""
    client = get_redis_client()
    if client is None:
        return None
    try:
        data = client.get(key)
        if data:
            logger.info(f"缓存命中: {key}")
            return json.loads(data)
    except Exception as e:
        logger.warning(f"缓存读取失败: {e}")
    return None


def set_cached(key: str, value: dict, ttl: int = 3600):
    """写入缓存"""
    client = get_redis_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, json.dumps(value, ensure_ascii=False))
        logger.info(f"缓存已写入: {key}")
    except Exception as e:
        logger.warning(f"缓存写入失败: {e}")


# 缓存 key 前缀
CACHE_PREFIX_PARSE = "resume:parse:"
CACHE_PREFIX_EXTRACT = "resume:extract:"
CACHE_PREFIX_MATCH = "resume:match:"
