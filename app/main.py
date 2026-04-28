from fastapi import FastAPI, Header, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.security import verify_internal_secret 
from app.config import settings
from app.prompt_builder import build_prompt
from app.openai_service import generate_job_description
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.models import JDRequest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# --- Health Endpoint ---
@app.get("/api/health")
def health():
    return {
        "status": "UP",
        "service": "hirescript-ai-service"
    }

# --- Generate Endpoint ---
@app.post("/api/ai/jd/generate")
@limiter.limit("4/minute")
def generate_jd(
    request: Request,
    payload: JDRequest,
    authorized: bool = Depends(verify_internal_secret)
):
    prompt = build_prompt(payload)

    try:
        result = generate_job_description(prompt)

        jd_content = result.get("content", "").strip()

        return {
            "status": "SUCCESS",
            "content": jd_content,
            "modelUsed": result.get("modelUsed", settings.OPENAI_MODEL),
            "promptVersion": settings.PROMPT_VERSION,
            "tokensUsed": result.get("tokensUsed")
        }

    except Exception as e:
        error_map = {
            "OPENAI_TIMEOUT": "OPENAI_TIMEOUT",
            "OPENAI_RATE_LIMIT": "RATE_LIMIT_EXCEEDED",
            "OPENAI_API_ERROR": "OPENAI_API_ERROR",
            "INTERNAL_SERVER_ERROR": "INTERNAL_SERVER_ERROR"
        }

        error_code = error_map.get(str(e), "INTERNAL_SERVER_ERROR")

        return JSONResponse(
            status_code=500,
            content={
                "status": "ERROR",
                "errorCode": error_code,
                "message": "Failed to generate job description"
            }
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract first meaningful error
    error_msg = exc.errors()[0]["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "status": "ERROR",
            "errorCode": "VALIDATION_ERROR",
            "message": error_msg
        },
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "status": "ERROR",
            "errorCode": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests. Please try again later."
        }
    )