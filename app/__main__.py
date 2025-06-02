import logging

import uvicorn

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting Blob service...")
    uvicorn.run("app.api:app", host="0.0.0.0", port=40000, reload=True)
