from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("yolov8s.pt")

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