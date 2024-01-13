from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.responses import Response, StreamingResponse

from app.log import logger
from app.schemas import SegmentationParams
from app.utils import process_image

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"message": "The API is up and running!"}


@router.post(
    "/segment-image",
    summary="Segment an uploaded image",
    description="Segment an uploaded image using the provided parameters. Returns the segmented image as a streaming response or an error response.",
    responses={
        200: {
            "description": "Segmented image as a streaming response",
            "content": {"image/png": {}},
        },
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def segment_image(
    request: Request,
    file: UploadFile = File(...),
    params: SegmentationParams = SegmentationParams(),
) -> Response:
    try:
        mask_generator = request.app.state.sam["mask_generator"]

        # Segment the image
        image = await process_image(file, params, mask_generator)

        return StreamingResponse(
            image, status_code=status.HTTP_200_OK, media_type="image/png"
        )
    except Exception as e:
        logger.error(
            f"[segment_image()] An error occured while processing the image: {e}"
        )
        return Response(
            {"message": "Something went wrong"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
