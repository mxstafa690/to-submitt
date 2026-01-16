from flask import Blueprint
from http import HTTPStatus
from sqlalchemy import text
from services.db import get_session

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint that verifies database connectivity.
    
    Returns:
        JSON with status (ok/degraded) and database connectivity info.
        HTTP 200 if healthy, 503 if database unavailable.
    """
    db_ok = True
    session = None
    try:
        session = get_session()
        session.execute(text("SELECT 1"))
    except Exception as e:
        db_ok = False
    finally:
        if session:
            session.close()
    
    status = "ok" if db_ok else "degraded"
    http_code = HTTPStatus.OK if db_ok else HTTPStatus.SERVICE_UNAVAILABLE
    
    return {
        "status": status,
        "database": "connected" if db_ok else "disconnected",
        "version": "1.0.0"
    }, http_code
