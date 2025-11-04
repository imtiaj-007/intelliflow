from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core import security_settings, settings
from app.db.session import db_session_manager
from app.middleware.auth import AuthMiddleware
from app.utils.logger import log


@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    log.info("🚀 Starting up IntelliFlow API...")
    async with db_session_manager.lifespan(app):
        yield
    log.info("🛑 Shutting down IntelliFlow API...")


def create_application() -> FastAPI:
    app = FastAPI(
        title="IntelliFlow",
        summary="A Visual Workflow Builder for Generative AI",
        description="IntelliFlow enables developers to design, test, and run AI-driven workflows using a visual canvas powered by React Flow and FastAPI. It connects components such as document knowledge bases, embeddings, and large language models (OpenAI, Gemini) to power dynamic, context-aware chat interfaces — all without writing glue code.",
        version="0.1.0",
        lifespan=combined_lifespan,
    )

    # Middlewares
    app.add_middleware(CORSMiddleware, **security_settings.get_cors_config())
    app.add_middleware(AuthMiddleware)

    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app


app = create_application()


@app.get(
    path="/",
    name="root",
    summary="Root endpoint",
    description="Returns the status of the IntelliFlow API service to confirm it is running properly",
)
def root_route():
    return {"status": "ok", "message": "IntelliFlow is live and running 🔮", "version": "0.1.0"}
