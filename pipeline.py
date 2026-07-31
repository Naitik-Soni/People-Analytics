from logger import logger

from modules.preprocessor import resize_frame_rf
from modules.object_detector import YOLODetector
from modules.object_tracker import BotSORTTracker
from modules.zone_counter import LineCounter
from modules.hourly_aggregator import HourlyAggregator

from config import config
from datetime import datetime

class AnalysisPipeline:
    def __init__(self):
        self.__frame_state = {}
        self.detector = YOLODetector()
        self.tracker = BotSORTTracker()
        self.counter = LineCounter(
            line_start=tuple(config.get("counter", "line_start")),
            line_end=tuple(config.get("counter", "line_end")),
        )
        self.aggregator = HourlyAggregator()
        logger.info("Initialized Analysis pipeline...")

    def process(self, frame, timestamp: datetime = None):
        resized_frame = resize_frame_rf(frame)
        self.__frame_state["frame"] = resized_frame

        detections = self.detector.detect(resized_frame)
        self.__frame_state["detected_objects"] = detections

        tracked = self.tracker.track(detections, resized_frame)
        self.__frame_state["tracked_objects"] = tracked

        counts = self.counter.update(tracked)
        self.__frame_state["counts"] = counts

        hourly = self.aggregator.update(counts, timestamp)
        self.__frame_state["current_hour"] = hourly

        return self.__frame_state