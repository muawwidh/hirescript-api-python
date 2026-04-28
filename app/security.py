from fastapi import Header, HTTPException
from app.config import settings


def verify_internal_secret(x_internal_secret: str = Header(None)):
    if not x_internal_secret:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "ERROR",
                "errorCode": "UNAUTHORIZED",
                "message": "Missing internal API secret"
            }
        )

    if x_internal_secret != settings.INTERNAL_API_SECRET:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "ERROR",
                "errorCode": "UNAUTHORIZED",
                "message": "Invalid internal API secret"
            }
        )

    return True