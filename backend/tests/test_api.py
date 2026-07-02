"""接口测试用例"""
import io
import fitz


def test_health(client):
    """测试健康检查"""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["code"] == "SUCCESS"
    assert data["data"]["status"] == "healthy"


def test_upload_invalid_type(client):
    """测试上传非 PDF 文件"""
    res = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
    )
    assert res.status_code == 400
    data = res.json()
    assert data["code"] == "INVALID_FILE_TYPE"


def test_upload_success(client, test_pdf_path):
    """测试上传 PDF 成功"""
    with open(test_pdf_path, "rb") as f:
        res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "resume_id" in data["data"]
    assert data["data"]["file_name"] == "resume.pdf"


def test_upload_duplicate(client, test_pdf_path):
    """测试重复上传同一文件"""
    resume_id_1 = None
    resume_id_2 = None

    with open(test_pdf_path, "rb") as f:
        res1 = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
        resume_id_1 = res1.json()["data"]["resume_id"]

    with open(test_pdf_path, "rb") as f:
        res2 = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
        resume_id_2 = res2.json()["data"]["resume_id"]

    assert resume_id_1 == resume_id_2


def test_parse_not_found(client):
    """测试解析不存在的简历"""
    res = client.post("/api/v1/resumes/res_not_exist/parse")
    assert res.status_code == 400
    assert res.json()["code"] == "RESOURCE_NOT_FOUND"


def test_parse_success(client, test_pdf_path):
    """测试解析简历成功"""
    # 先上传
    with open(test_pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
    resume_id = upload_res.json()["data"]["resume_id"]

    # 解析
    res = client.post(f"/api/v1/resumes/{resume_id}/parse")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "basic_info" in data["data"]
    assert "skills" in data["data"]
    assert "raw_text" in data["data"]
    assert "cleaned_text" in data["data"]


def test_match_not_found(client):
    """测试匹配不存在的简历"""
    res = client.post(
        "/api/v1/match",
        json={"resume_id": "res_not_exist", "job_description": "Python 工程师"},
    )
    assert res.status_code == 400
    assert res.json()["code"] == "RESOURCE_NOT_FOUND"


def test_match_unparsed(client, test_pdf_path):
    """测试匹配未解析的简历"""
    # 上传但不解析
    with open(test_pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
    resume_id = upload_res.json()["data"]["resume_id"]

    res = client.post(
        "/api/v1/match",
        json={"resume_id": resume_id, "job_description": "Python 工程师"},
    )
    assert res.status_code == 400
    assert res.json()["code"] == "RESOURCE_NOT_FOUND"


def test_match_success(client, test_pdf_path):
    """测试匹配评分成功"""
    # 上传 + 解析
    with open(test_pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
    resume_id = upload_res.json()["data"]["resume_id"]
    client.post(f"/api/v1/resumes/{resume_id}/parse")

    # 匹配
    res = client.post(
        "/api/v1/match",
        json={
            "resume_id": resume_id,
            "job_description": "招聘 Python 后端工程师，要求熟悉 FastAPI、MySQL、Redis",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "analysis_id" in data["data"]
    assert "match_result" in data["data"]
    assert data["data"]["match_result"]["match_score"] >= 0
    assert data["data"]["match_result"]["score_level"] in ("high", "medium", "low")


def test_match_validation_error(client):
    """测试匹配参数校验失败"""
    res = client.post("/api/v1/match", json={})
    assert res.status_code == 422


def test_history_empty(client):
    """测试历史记录为空"""
    # 注意：由于前面的测试可能已经创建了记录，这里只验证接口可用
    res = client.get("/api/v1/analysis/history")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_history_pagination(client):
    """测试历史记录分页"""
    res = client.get("/api/v1/analysis/history?page=1&page_size=5")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5


def test_analysis_detail_not_found(client):
    """测试查询不存在的分析记录"""
    res = client.get("/api/v1/analysis/ana_not_exist")
    assert res.status_code == 400
    assert res.json()["code"] == "RESOURCE_NOT_FOUND"


def test_analysis_detail_success(client, test_pdf_path):
    """测试查询分析详情成功"""
    # 完整流程
    with open(test_pdf_path, "rb") as f:
        upload_res = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.pdf", f, "application/pdf")},
        )
    resume_id = upload_res.json()["data"]["resume_id"]
    client.post(f"/api/v1/resumes/{resume_id}/parse")

    match_res = client.post(
        "/api/v1/match",
        json={"resume_id": resume_id, "job_description": "Python 工程师"},
    )
    analysis_id = match_res.json()["data"]["analysis_id"]

    # 查询详情
    res = client.get(f"/api/v1/analysis/{analysis_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["data"]["id"] == analysis_id
    assert "job_analysis" in data["data"]
    assert "match_result" in data["data"]
    assert "resume_data" in data["data"]


def test_upload_page_limit(client):
    """测试上传超过 5 页的 PDF"""
    doc = fitz.open()
    for i in range(6):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i + 1}")
    pdf_bytes = doc.tobytes()
    doc.close()

    res = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("6pages.pdf", pdf_bytes, "application/pdf")},
    )
    assert res.status_code == 400
    assert res.json()["code"] == "PDF_PAGE_LIMIT_EXCEEDED"
