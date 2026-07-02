from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.match import router as match_router
from app.api.v1.analysis import router as analysis_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(resumes_router, prefix="/resumes", tags=["resumes"])
api_router.include_router(match_router, prefix="/match", tags=["match"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
