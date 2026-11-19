import os
from urllib.parse import urlsplit

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analytics import router as analytics_router
from app.api.data import router as data_router
from app.api.business import router as business_router


def _cors_origins() -> list[str]:
    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "").strip()
    if not frontend_origin:
        return origins

    frontend_origin = frontend_origin.rstrip("/")
    parsed = urlsplit(frontend_origin)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError("FRONTEND_ORIGIN must be an HTTP(S) origin without a path.")
    try:
        parsed.port
    except ValueError as error:
        raise ValueError("FRONTEND_ORIGIN must contain a valid port.") from error

    origins.append(frontend_origin)
    return origins


app = FastAPI(
    title="Afficionado Intelligence API",
    version="0.1.0",
    description="Data-driven retail product intelligence platform",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(business_router, prefix="/api")


@app.get("/api/health")
def health() -> dict:
    return {"status": "healthy", "service": "afficionado-intelligence"}
