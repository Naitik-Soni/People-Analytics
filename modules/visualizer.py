import cv2

from config import config
from logger import logger

def visualize(frame_context: dict, vis_det: bool = False, vis_track: bool = True):
    frame = frame_context.get("frame")
    box_color = tuple(config.get("bounding_box_color"))

    if vis_track:
        tracked_objects = frame_context.get("tracked_objects", [])
        for track in tracked_objects:
            x1, y1, x2, y2, track_id = map(int, track[:5])
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, f"Id: {track_id}", (x1, y1 - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, box_color, 1)

    if vis_det:
        detected_objects = frame_context.get("detected_objects", [])
        for det in detected_objects:
            x1, y1, x2, y2 = map(int, det[:4])
            conf = float(det[4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, f"Conf: {conf:.2f}", (x1, y1 - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, box_color, 1)

    line_start = tuple(config.get("counter", "line_start"))
    line_end = tuple(config.get("counter", "line_end"))
    cv2.line(frame, line_start, line_end, (0, 255, 255), 2)

    counts = frame_context.get("counts", {})
    cv2.putText(
        frame,
        f"IN: {counts.get('in_count', 0)}  OUT: {counts.get('out_count', 0)}",
        (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (0, 255, 255), 2
    )

    cv2.imshow("Video analytics", frame)

    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        return True
    return False