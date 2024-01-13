from io import BytesIO
from pathlib import Path
from typing import Tuple

import numpy as np
import torch
from fastapi import UploadFile
from mobile_sam import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry
from PIL import Image

from app.log import logger
from app.mobilesam.tools import fast_process
from app.schemas import SegmentationParams


def get_device() -> str:
    """
    Get the device for PyTorch computations.

    Returns:
        str: Device ('cuda' or 'cpu').
    """
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def initialize_mobile_sam() -> Tuple[SamAutomaticMaskGenerator, SamPredictor]:
    """
    Initialize the MobileSAM model.

    Returns:
        Tuple[SamAutomaticMaskGenerator, SamPredictor]: Tuple containing instances of SamAutomaticMaskGenerator and SamPredictor.
    """
    device = get_device()

    sam_checkpoint = Path(__file__).parent / "mobilesam/mobile_sam.pt"
    model_type = "vit_t"

    mobile_sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    mobile_sam = mobile_sam.to(device=device)
    mobile_sam.eval()

    mask_generator = SamAutomaticMaskGenerator(mobile_sam)
    predictor = SamPredictor(mobile_sam)

    return mask_generator, predictor


def resize_image(image: Image.Image, size: int) -> Image.Image:
    """
    Resize the given image.

    Args:
        image (Image.Image): The input image.
        size (int): The input size.

    Returns:
        Image.Image: Resized image.
    """
    w, h = image.size
    scale = size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    image = image.resize((new_w, new_h))
    return image


@torch.no_grad()
async def process_image(
    file: UploadFile,
    params: SegmentationParams,
    mask_generator: SamAutomaticMaskGenerator,
) -> BytesIO:
    """
    Process an uploaded image file.

    Args:
        file (UploadFile): The uploaded image file.
        params (SegmentationParams): Segmentation parameters.
        mask_generator (SamAutomaticMaskGenerator): Instance of the mask generator.

    Returns:
        BytesIO: A BytesIO object containing the processed image in PNG format.
    """
    try:
        # Read and resize the image
        image_content = await file.read()
        image = Image.open(BytesIO(image_content)).convert("RGB")
        image = resize_image(image, params.input_size)

        # Generate annotations
        nd_image = np.array(image)
        annotations = mask_generator.generate(nd_image)

        # Create a segmented figure
        fig = fast_process(
            annotations=annotations,
            image=image,
            device=get_device(),
            scale=(1024 // params.input_size),
            better_quality=params.better_quality,
            mask_random_color=params.mask_random_color,
            bbox=None,
            use_retina=params.use_retina,
            withContours=params.with_contours,
        )

        # Save the figure as a PNG image and return it as a BytesIO object
        buf = BytesIO()
        fig.save(buf, format="PNG")
        byte_im = buf.getvalue()
        buf.close()

        return BytesIO(byte_im)

    except Exception as e:
        logger.error(
            f"[process_image()] An error occured while processing the uploaded image: {e}"
        )
        raise e
