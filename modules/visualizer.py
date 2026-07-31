import cv2

from config import config
from logger import logger

def visualize(frame_context: dict, vis_det: bool=False, vis_track: bool=True):

    frame = frame_context.get("frame")

    if vis_track:
        tracked_objects = frame_context.get("tracked_objects")

        for object in tracked_objects:
            x1, y1, x2, y2, id = map(int, object[:5])
            cv2.rectangle(frame, (x1, y1), (x2, y2), tuple(config.get("bounding_box_color")), 2)
            cv2.putText(frame, f"Id: {id}", (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, config.get("bounding_box_color"), 1)

    if vis_det:
        detected_objects = frame_context.get("detected_objects")

        for object in detected_objects:
            x1, y1, x2, y2, conf = map(int, object[:5])
            cv2.rectangle(frame, (x1, y1), (x2, y2), tuple(config.get("bounding_box_color")), 2)
            cv2.putText(frame, f"Conf: {conf}", (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, config.get("bounding_box_color"), 1)

    cv2.imshow("Video analytics", frame)

    if cv2.waitKey(1) and 0xFF == ord("q"):
        return True
    return False