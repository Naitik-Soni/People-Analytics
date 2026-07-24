import cv2
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
        self.model = model
        self.confidence_thresh = confidence_thresh
        self.device = device
        self.classes = classes

    def detect(self, frame):
        predictions = self._predict(frame)

        predicted_boxes = predictions.boxes.xyxy.cpu().numpy()
        prediction_confidence = predictions.boxes.conf.cpu().numpy()
        predicted_classes = predictions.boxes.cls.cpu().numpy()

        detections = np.column_stack([
            predicted_boxes,
            prediction_confidence[:, None],
            predicted_classes[:, None]
        ])

        return detections

    def _predict(self, frame):
        predictions = self.model.predict(
                                frame,
                                conf=self.confidence_thresh,
                                device=self.device,
                                verbose=False,
                                classes=self.classes
                            )
        
        return predictions[0]


def detect_objects(frame, conf=0.5, display=False):
    detections = detect_with_yolo(frame, conf, display)
    return np.asarray(detections, dtype=np.float32)


def detect_with_yolo(frame, conf=0.5, display=False):
    results = model.predict(frame, conf=conf, device="cpu", verbose=False, classes=[0])

    detections = []

    result = results[0]
    boxes = result.boxes.xyxy.cpu().numpy()
    scores = result.boxes.conf.cpu().numpy()
    classes = result.boxes.cls.cpu().numpy()

    for box, score, cls in zip(boxes, scores, classes):
        x1, y1, x2, y2 = box[:4].astype(int)
        detections.append([x1, y1, x2, y2, score, cls])

        if display:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if display:
        cv2.imshow("Detections", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return detections


# IMG_PATH = r"C:\Users\baps\Documents\Projects\Tracking\Research\Object counter\image-1.webp"
# image = cv2.imread(IMG_PATH)
# print(detect_objects(image, display=True))