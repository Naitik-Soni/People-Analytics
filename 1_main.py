import cv2

# Main function for starting the analytics process
def main(VIDEO_PATH: str):
    video_capture = cv2.VideoCapture(VIDEO_PATH)

    fps = int(video_capture.get(5))

    is_frame_available, frame = video_capture.read()

    if not is_frame_available:
        print("Video is not available")
        return
    
    while True:
        is_frame_available, frame = video_capture.read()

        if not is_frame_available:
            print("Next frame not available")
            break
        
        process_frame(frame)

    cv2.destroyAllWindows()
    video_capture.release()


if __name__ == "__main__":
    VIDEO_PATH = r"C:\Users\baps\Documents\Projects\Tracking\Production\Mall-surveillance\Data\Vid-1.mkv"
    main(VIDEO_PATH)