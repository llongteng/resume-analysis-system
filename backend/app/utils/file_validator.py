import hashlib
import io

import fitz  # PyMuPDF

from app.core.errors import InvalidFileTypeError, FileTooLargeError, PDFPageLimitError
from app.core.logging import logger

ALLOWED_EXTENSIONS = {".pdf"}
ALLOWED_MIME_TYPES = {"application/pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_PAGES = 5


def validate_pdf_file(file_name: str, file_size: int, file_content: bytes, content_type: str | None = None):
    """
    校验上传的 PDF 文件（扩展名、MIME、大小、页数）。

    Args:
        file_name: 文件名
        file_size: 文件大小（字节）
        file_content: 文件内容（用于页数校验）
        content_type: MIME 类型

    Raises:
        InvalidFileTypeError: 文件类型不合法
        FileTooLargeError: 文件过大
        PDFPageLimitError: 页数超限
    """
    # 校验扩展名
    ext = "." + file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"文件扩展名校验失败: {file_name}")
        raise InvalidFileTypeError()

    # 校验 MIME 类型
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        logger.warning(f"文件 MIME 类型校验失败: {content_type}")
        raise InvalidFileTypeError()

    # 校验文件大小
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"文件大小超限: {file_size} bytes")
        raise FileTooLargeError()

    # 校验页数
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        page_count = len(doc)
        doc.close()
        if page_count > MAX_PAGES:
            logger.warning(f"PDF 页数超限: {page_count} 页")
            raise PDFPageLimitError()
    except PDFPageLimitError:
        raise
    except Exception as e:
        logger.warning(f"PDF 页数校验失败（文件可能损坏）: {e}")
        raise InvalidFileTypeError()


def compute_file_hash(file_content: bytes) -> str:
    """计算文件的 SHA256 哈希"""
    return hashlib.sha256(file_content).hexdigest()
