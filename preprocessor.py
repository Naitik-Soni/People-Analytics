"""Video frame preprocessor for preprocessing the frame before analysis pipeline"""
import cv2
from cv2.typing import MatLike

from config import config
from logger import logger

# Function used to resize the frame with specific height and width
def resize_frame(frame: MatLike , new_size: tuple = (1024, 1024)):
    logger.debug(f"Resizing the frame with size={new_size}")
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_LINEAR)

# Function used to resize the frame with specific resize factor
def resize_frame(frame: MatLike , resize_factor: float = config.get("resize_factor")):
    height, width = frame.shape[:2]
    new_height, new_width = int(height*resize_factor), int(width*resize_factor)
    logger.debug(f"Resizing the frame with factor={resize_factor}")
    return cv2.resize(frame, (new_width, new_height))