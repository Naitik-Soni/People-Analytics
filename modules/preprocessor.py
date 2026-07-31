"""Video frame preprocessor for preprocessing the frame before analysis pipeline"""
import cv2
from cv2.typing import MatLike

from config import config
from logger import logger

def resize_frame_s(frame, new_size: tuple = (1024, 1024)) -> MatLike:
    try:
        logger.debug("Resizing frame to {}", new_size)
        return cv2.resize(frame, new_size, interpolation=cv2.INTER_LINEAR)
    except Exception:
        logger.exception("Failed to resize frame to {}", new_size)
        raise

def resize_frame_rf(frame, resize_factor: float = None) -> MatLike:
    try:
        if resize_factor is None:
            resize_factor = config.get("resize_factor")

        height, width = frame.shape[:2]
        new_height, new_width = int(height * resize_factor), int(width * resize_factor)
        logger.debug(f"Resizing the frame with factor={resize_factor}")
        return cv2.resize(frame, (new_width, new_height))
    except Exception:
        logger.exception("Failed to resize frame with {}", resize_factor)
        raise