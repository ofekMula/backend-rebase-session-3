import logging

from fastapi import FastAPI

from app.endpoints import blobs_router

logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


app = FastAPI()


app.include_router(blobs_router, prefix="/api/v1", tags=["blobs"])
