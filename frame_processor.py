import cv2
from boxmot import BotSort
from object_detector import detect_objects


tracker = BotSort(
    reid_weights="osnet_x0_25_msmt17.pt",   # Path to ReID weights
    device="cpu",                        # or "cpu"
    half=False,                              # False if using CPU

    track_high_thresh=0.5,
    track_low_thresh=0.1,
    new_track_thresh=0.6,
    match_thresh=0.8,
    track_buffer=30,
    frame_rate=30,
)

def resize_frame(frame, resize_factor=0.75):
    height, width = frame.shape[:2]
    return cv2.resize(frame, (int(width*resize_factor), int(height*resize_factor)))

def process_frame(frame):

    frame = resize_frame(frame)
    overlay = frame.copy()
    alpha = 0.05

    detections = detect_objects(frame, conf=0.2)

    tracked_objects = tracker.update(detections, frame)

    l_det = len(detections)
    l_tra = len(tracked_objects)

    # for detection in detections:
    #     detection = detection.astype(int).tolist()
    #     x1, y1, x2, y2 = detection[:4]
    #     cv2.rectangle(
    #         overlay,
    #         (int(x1), int(y1)),
    #         (int(x2), int(y2)),
    #         (0, 255, 0),
    #         -1
    #     )
    #     cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    #     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)

    for tracked_object in tracked_objects:
        tracked_object = tracked_object.astype(int).tolist()
        x1, y1, x2, y2 = tracked_object[:4]
        id = tracked_object[4]
        cv2.rectangle(
                    overlay,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    -1
                )
        cv2.putText(frame, f"ID-{id}", (x1-15, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)

    cv2.rectangle(frame, (12, 12), (450, 40), (255,255,0), -1)
    cv2.putText(frame, f"DetCount - {l_det}, TrackCount - {l_tra}", (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    