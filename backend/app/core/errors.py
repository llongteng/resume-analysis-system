from enum import Enum


class ErrorCode(str, Enum):
    SUCCESS = "SUCCESS"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    PDF_PAGE_LIMIT_EXCEEDED = "PDF_PAGE_LIMIT_EXCEEDED"
    PDF_PARSE_FAILED = "PDF_PARSE_FAILED"
    AI_EXTRACT_FAILED = "AI_EXTRACT_FAILED"
    AI_RESPONSE_INVALID = "AI_RESPONSE_INVALID"
    AI_MATCH_FAILED = "AI_MATCH_FAILED"
    MATCH_FAILED = "MATCH_FAILED"
    CACHE_UNAVAILABLE = "CACHE_UNAVAILABLE"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.SUCCESS: "操作成功",
    ErrorCode.INVALID_FILE_TYPE: "仅支持上传 PDF 文件",
    ErrorCode.FILE_TOO_LARGE: "文件大小超过限制，最大 10MB",
    ErrorCode.PDF_PAGE_LIMIT_EXCEEDED: "PDF 页数超过限制，最多 5 页",
    ErrorCode.PDF_PARSE_FAILED: "PDF 文本解析失败",
    ErrorCode.AI_EXTRACT_FAILED: "AI 简历信息提取失败",
    ErrorCode.AI_RESPONSE_INVALID: "AI 返回格式错误",
    ErrorCode.AI_MATCH_FAILED: "AI 岗位匹配失败",
    ErrorCode.MATCH_FAILED: "匹配评分失败",
    ErrorCode.CACHE_UNAVAILABLE: "缓存服务不可用",
    ErrorCode.RESOURCE_NOT_FOUND: "资源不存在",
    ErrorCode.VALIDATION_ERROR: "请求参数校验失败",
    ErrorCode.INTERNAL_ERROR: "服务内部错误",
}


class BusinessError(Exception):
    """业务异常基类"""

    def __init__(self, code: ErrorCode, message: str | None = None):
        self.code = code
        self.message = message or ERROR_MESSAGES.get(code, "未知错误")
        super().__init__(self.message)


class InvalidFileTypeError(BusinessError):
    def __init__(self):
        super().__init__(ErrorCode.INVALID_FILE_TYPE)


class FileTooLargeError(BusinessError):
    def __init__(self):
        super().__init__(ErrorCode.FILE_TOO_LARGE)


class PDFPageLimitError(BusinessError):
    def __init__(self):
        super().__init__(ErrorCode.PDF_PAGE_LIMIT_EXCEEDED)


class PDFParseError(BusinessError):
    def __init__(self, detail: str | None = None):
        super().__init__(ErrorCode.PDF_PARSE_FAILED, detail)


class AIExtractError(BusinessError):
    def __init__(self, detail: str | None = None):
        super().__init__(ErrorCode.AI_EXTRACT_FAILED, detail)


class ResourceNotFoundError(BusinessError):
    def __init__(self, detail: str | None = None):
        super().__init__(ErrorCode.RESOURCE_NOT_FOUND, detail)
