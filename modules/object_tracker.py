from boxmot import BotSort

from config import config
from logger import logger

# BotSORT tracker class for tracking objects
class BotSORTTracker:
    def __init__(self):
        try:
            self.tracker = BotSort(
                                reid_weights=config.get("tracker", "botsort", "reid_weights"),   
                                device=config.get("device"),                     
                                half=config.get("tracker", "botsort", "half"), 
                                track_high_thresh=config.get("tracker", "botsort", "track_high_thresh"),
                                track_low_thresh=config.get("tracker", "botsort", "track_low_thresh"),
                                new_track_thresh=config.get("tracker", "botsort", "new_track_thresh"),
                                match_thresh=config.get("tracker", "botsort", "match_thresh"),
                                track_buffer=config.get("tracker", "botsort", "track_buffer"),
                                frame_rate=config.get("tracker", "botsort", "frame_rate"),
                            )
            logger.info("BotSORT tracker initialized...")
        except Exception:
            logger.exception("Error in BotSORT initialization")
            raise

    # Tracking and updating the current tracks
    def track(self, detections, frame):
        try:
            tracked_objects = self.tracker.update(detections, frame)
            logger.debug("Tracked objects of length {}", len(tracked_objects))
            return tracked_objects
        except Exception:
            logger.exception("Error in tracking objects")
            raise