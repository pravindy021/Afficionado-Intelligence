from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analytics import router as analytics_router
from app.api.data import router as data_router
from app.api.business import router as business_router

app = FastAPI(
    title="Afficionado Intelligence API",
    version="0.1.0",
    description="Data-driven retail product intelligence platform",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
