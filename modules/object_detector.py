"""Object detector"""
import numpy as np
from ultralytics import YOLO

from config import config
from logger import logger

class YOLODetector:
    def __init__(self, model=None, confidence_thresh: float = None, device=None, classes=None):
        self.model = YOLO(model or config.get("detector"))
        self.confidence_thresh = confidence_thresh if confidence_thresh is not None else config.get("detection_conf")
        self.device = device or config.get("device")
        self.classes = classes if classes is not None else config.get("data_type", "coco8", "classes")

        logger.info(
            "Yolo model loaded with config thresh={}, classes={}",
            self.confidence_thresh, self.classes
        )

    def detect(self, frame):
        try:
            predictions = self._predict(frame)

            predicted_boxes = predictions.boxes.xyxy.cpu().numpy()
            prediction_confidence = predictions.boxes.conf.cpu().numpy()
            predicted_classes = predictions.boxes.cls.cpu().numpy()

            detections = np.column_stack([
                predicted_boxes,
                prediction_confidence[:, None],
                predicted_classes[:, None]
            ])

            logger.debug("Number of objects detected for the frame: {}", len(detections))

            return detections
        except Exception:
            logger.exception("Error in detecting object with Yolo")
            raise

    def _predict(self, frame):
        predictions = self.model.predict(
            frame,
            conf=self.confidence_thresh,
            device=self.device,
            verbose=False,
            classes=self.classes
        )
        return predictions[0]