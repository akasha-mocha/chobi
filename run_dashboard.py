import uvicorn
from scripts.utils.logger import get_logger

from dashboard.server import app


logger = get_logger("dashboard")


def main():

    logger.info("Starting Dev Command Center")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":

    main()