import logging
import sys

from app.core.config import get_settings


def setup_logging() -> logging.Logger:
    settings = get_settings()
    level = logging.DEBUG if settings.APP_DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger("resume_analyzer")
    logger.setLevel(level)
    logger.addHandler(handler)

    # 避免 uvicorn 日志重复
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn.access").handlers.clear()

    return logger


logger = setup_logging()
