import json
import re
import time

from openai import OpenAI

from app.core.config import get_settings
from app.core.logging import logger

MAX_RETRIES = 3


def get_ai_client() -> OpenAI:
    """获取 AI 客户端（惰性初始化）"""
    settings = get_settings()
    return OpenAI(
        api_key=settings.AI_API_KEY,
        base_url=settings.AI_BASE_URL,
        timeout=settings.AI_TIMEOUT,
    )


def call_ai_json(system_prompt: str, user_prompt: str) -> dict:
    """
    调用 AI 模型，要求返回 JSON。

    带重试机制：最多重试 3 次，指数退避。

    Args:
        system_prompt: 系统提示词
        user_prompt: 用户输入

    Returns:
        解析后的 JSON dict

    Raises:
        Exception: 重试耗尽后仍失败
    """
    settings = get_settings()
    client = get_ai_client()
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"调用 AI 模型: {settings.AI_MODEL_NAME} (第 {attempt + 1} 次)")

            response = client.chat.completions.create(
                model=settings.AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("AI 返回内容为空")

            logger.info(f"AI 返回内容长度: {len(content)} 字符")
            return parse_ai_json(content)

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt
                logger.warning(f"AI 调用失败，{wait}s 后重试: {e}")
                time.sleep(wait)
            else:
                logger.error(f"AI 调用失败，已重试 {MAX_RETRIES} 次: {e}")

    raise last_error


def parse_ai_json(text: str) -> dict:
    """
    从 AI 返回文本中提取 JSON。

    支持:
    1. 直接 JSON
    2. Markdown 代码块中的 JSON
    3. 带前后文字的 JSON
    """
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试从 markdown 代码块提取
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # 尝试找到第一个 { 和最后一个 }
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"无法从 AI 返回中提取 JSON: {text[:200]}...")
