from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from scripts.utils.logger import get_logger
from dashboard.api.api import api as api_router
from dashboard.services.ws_manager import manager

logger = get_logger("dashboard_server")

ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT / "dashboard" / "static"


def create_app():

    app = FastAPI(
        title="AI Dev Command Center",
        version="1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        api_router,
        prefix="/api"
    )

    app.mount(
        "/",
        StaticFiles(directory=str(STATIC_DIR), html=True),
        name="dashboard"
    )

    @app.on_event("startup")
    async def startup_event():
        logger.info("Dev Command Center started")

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "service": "ai-dev-dashboard"
        }

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):

        await manager.connect(ws)

        try:
            while True:
                await ws.receive_text()

        except Exception:
            logger.info("WebSocket client disconnected")

        finally:
            manager.disconnect(ws)

    return app


app = create_app()


async def broadcast(data: dict):
    await manager.broadcast(data)