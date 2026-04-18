from src.config import (
    CAMERA_HEIGHT,
    CAMERA_ID,
    CAMERA_WIDTH,
    CONFIDENCE_THRESHOLD,
    MODEL_PATH,
)
from src.detector import Camera, Detection

if __name__ == "__main__":
    camera = Camera(CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT)
    detector = Detection(MODEL_PATH, CONFIDENCE_THRESHOLD)

    def process_frame():
        camera.read_frame()

        if camera.connected is True:
            detector.get_detected_objects(camera.frame)
            detector.draw_detected_objects(camera.frame)

        return camera.frame
    
    camera.run(process_frame)