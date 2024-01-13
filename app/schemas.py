from pydantic import BaseModel


class SegmentationParams(BaseModel):
    """Parameters for image segmentation"""

    input_size: int = 1024
    better_quality: bool = False
    with_contours: bool = True
    use_retina: bool = True
    mask_random_color: bool = True
