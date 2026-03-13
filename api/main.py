from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.deps import model_service
from api.routes.financials import router as financials_router
from api.routes.forecast import router as forecast_router
from api.routes.health import router as health_router
from api.routes.production import router as production_router
from api.routes.report import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_service.load()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(forecast_router, prefix=settings.api_prefix)
app.include_router(production_router, prefix=settings.api_prefix)
app.include_router(financials_router, prefix=settings.api_prefix)
app.include_router(report_router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {
        "message": "Global Solar Platform API running",
        "docs": "/docs",
        "version": settings.app_version,
    }
