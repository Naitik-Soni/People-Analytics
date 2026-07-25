import cv2

from config import config
from logger import logger
from pipeline import AnalysisPipeline


# Main function for starting the analytics process
def main():
    video_path = config.get("video_path")
    video_capture = cv2.VideoCapture(video_path)

    is_video_available = video_capture.isOpened()

    frame_counter = 0

    pipeline = AnalysisPipeline()

    if not is_video_available:
        logger.warning("Video not found on {}", video_path)
        return
    
    while True:
        is_frame_available, frame = video_capture.read()

        if not is_frame_available:
            logger.info("Next frame not found in the video={}", video_path)
            break

        frame_counter += 1

        if frame_counter % 2 == 0:
            continue

        pipeline.process(frame)

        if config.get("debug"):
            cv2.imshow("Original Video", frame)
            if cv2.waitKey(1) and 0xFF == ord("q"):
                break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()