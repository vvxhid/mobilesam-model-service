from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.utils import initialize_mobile_sam


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for managing the lifespan of resources during FastAPI application startup and shutdown.
    """
    try:
        # Startup: Initialize and set up resources
        mask_generator, _ = initialize_mobile_sam()
        app.state.sam = {}
        app.state.sam["mask_generator"] = mask_generator

        # Yield control to the caller
        yield

    finally:
        # Shutdown: Clean up resources
        app.state.sam.clear()


app = FastAPI(
    title="MobileSam Segmentation Model Service",
    description="MobileSam is a machine learning model specialized in image segmentation on CPUs.",
    lifespan=lifespan,
    root_path="/api"
)

# Allow CORS for local debugging
app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(router)
