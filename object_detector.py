import numpy as np
from ultralytics import YOLO

from config import config
from logger import logger

class YOLODetector():
    def __init__(
            self,
            model = config.get("detector"),
            confidence_thresh: float = config.get("detection_conf"),
            device = config.get("device"),
            classes = config.get("data_type", "coco8", "classes")
        ):
        self.model = YOLO(model)
        self.confidence_thresh = confidence_thresh
        self.device = device
        self.classes = classes
        logger.info("Yolo model {} loaded with config thresh={}, classes={}", model, confidence_thresh, classes)

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

            logger.debug("Number of objects detected for the frame ", len(detections))

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

# Uncomment below line for testing
# IMG_PATH = r"image.png"
# image = cv2.imread(IMG_PATH)

# detector = YOLODetector()
# detections = detector.detect(image)

# print(detections)
# print(type(detections))