import re
import fitz  # PyMuPDF

from app.core.errors import PDFParseError, PDFPageLimitError
from app.core.logging import logger

MAX_PAGES = 5


def extract_text_from_pdf(file_path: str) -> tuple[str, list[str]]:
    """
    从 PDF 文件中提取文本。

    Args:
        file_path: PDF 文件路径

    Returns:
        (raw_text, pages_text): 原始合并文本 和 每页文本列表

    Raises:
        PDFPageLimitError: 页数超过限制
        PDFParseError: 解析失败
    """
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise PDFParseError(f"无法打开 PDF 文件: {e}")

    try:
        page_count = len(doc)
        # 防御性检查（upload 阶段已校验，此处防止绕过直接调用）
        if page_count > MAX_PAGES:
            raise PDFPageLimitError()

        pages_text = []
        for page in doc:
            text = page.get_text()
            pages_text.append(text)

        raw_text = "\n".join(pages_text)
        logger.info(f"PDF 解析完成: {page_count} 页, {len(raw_text)} 字符")
        return raw_text, pages_text

    finally:
        doc.close()


def clean_resume_text(raw_text: str) -> str:
    """
    清洗简历文本。

    规则:
    1. 去除多余空格（保留单个空格）
    2. 去除重复换行（合并为单个换行）
    3. 合并无意义断行（非标点结尾的短行合并到上一行）
    4. 保留邮箱、手机号、项目符号等关键信息
    5. 去除首尾空白
    """
    text = raw_text

    # 1. 将 \r\n 和 \r 统一为 \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 2. 去除每行首尾空格
    lines = [line.strip() for line in text.split("\n")]

    # 3. 合并无意义断行：如果一行很短（<15字符）且不以标点结尾，合并到上一行
    merged_lines = []
    for line in lines:
        if not line:
            merged_lines.append("")
            continue

        # 判断是否是独立行（以标点、项目符号、数字编号开头等）
        is_independent = bool(re.match(r'^[\d•\-·●◆▪▸►①②③④⑤⑥⑦⑧⑨⑩]', line))
        ends_with_punctuation = bool(re.search(r'[。！？.!?:：;；）)]$', line))

        if (
            merged_lines
            and merged_lines[-1]
            and not is_independent
            and not ends_with_punctuation
            and len(line) < 15
        ):
            # 合并到上一行
            merged_lines[-1] = merged_lines[-1] + " " + line
        else:
            merged_lines.append(line)

    # 4. 去除连续空行（保留最多一个）
    result_lines = []
    prev_empty = False
    for line in merged_lines:
        if not line:
            if not prev_empty:
                result_lines.append("")
            prev_empty = True
        else:
            result_lines.append(line)
            prev_empty = False

    # 5. 去除多余空格
    cleaned = "\n".join(result_lines)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    cleaned = cleaned.strip()

    logger.info(f"文本清洗完成: {len(raw_text)} -> {len(cleaned)} 字符")
    return cleaned
