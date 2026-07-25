from logger import logger

from modules.preprocessor import *
from modules.object_detector import YOLODetector
from modules.object_tracker import BotSORTTracker

class AnalysisPipeline:
    def __init__(self):
        self.__context_manager = {}
        self.detector = YOLODetector()
        self.tracker = BotSORTTracker()
        logger.info("Initialized Analysis pipeline...")


    def process(self, frame):

        resize_frame = resize_frame(frame, 1)
