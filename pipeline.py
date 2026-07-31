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

        resized_frame = resize_frame_rf(frame)
        self.__context_manager["frame"] = resized_frame

        detections = self.detector.detect(resized_frame)
        self.__context_manager["detected_objects"] = detections

        tracked = self.tracker.track(detections, resized_frame)
        self.__context_manager["tracked_objects"] = tracked

        return self.__context_manager
