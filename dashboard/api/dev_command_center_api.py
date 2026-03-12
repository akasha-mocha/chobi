from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from scripts.utils.logger import get_logger
from dashboard.api.api import api as api_router

logger = get_logger("dashboard_server")

# ---------------------------------------
# Path Resolve
# ---------------------------------------

ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = ROOT / "dashboard" / "static"

# ---------------------------------------
# WebSocket clients
# ---------------------------------------

clients = []

# ---------------------------------------
# FastAPI App
# ---------------------------------------


def create_app():

    app = FastAPI(
        title="AI Dev Command Center",
        version="1.0"
    )

    # ----------------------------
    # CORS
    # ----------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----------------------------
    # API Router
    # ----------------------------

    app.include_router(
        api_router,
        prefix="/api"
    )

    # ----------------------------
    # Static UI
    # ----------------------------

    app.mount(
        "/",
        StaticFiles(directory=str(STATIC_DIR), html=True),
        name="dashboard"
    )

    # ----------------------------
    # Startup
    # ----------------------------

    @app.on_event("startup")
    async def startup_event():

        logger.info("Dev Command Center started")

    # ----------------------------
    # Health Check
    # ----------------------------

    @app.get("/health")
    async def health():

        return {
            "status": "ok",
            "service": "ai-dev-dashboard"
        }

    # ----------------------------
    # WebSocket
    # ----------------------------

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):

        await ws.accept()
        clients.append(ws)

        logger.info("WebSocket client connected")

        try:

            while True:
                try:
                	await ws.receive_text()
                except Exception:
                	break

        except Exception:

            logger.info("WebSocket client disconnected")

        finally:

            if ws in clients:
                clients.remove(ws)

    return app


app = create_app()


# ---------------------------------------
# Broadcast helper
# ---------------------------------------

async def broadcast(data: dict):

    dead = []

    for c in clients:

        try:
            await c.send_json(data)

        except Exception:
            dead.append(c)

    for d in dead:

        if d in clients:
            clients.remove(d)