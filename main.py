from src.config import (
    CAMERA_HEIGHT,
    CAMERA_ID,
    CAMERA_WIDTH,
    CONFIDENCE_THRESHOLD,
    MODEL_PATH,
)
from src.detector import Camera, Detection

camera = Camera(CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT)
detector = Detection(MODEL_PATH, CONFIDENCE_THRESHOLD)


frame_counter = 0

def process_frame():
    global frame_counter
    
    frame = camera.read_frame()
    
    if not camera.connected:
        return frame

    if frame_counter % 5 == 0:
        detector.get_detected_objects(frame)

    if detector.results:
        detector.draw_detected_objects(frame)
        
    frame_counter += 1
    
    return frame

if __name__ == "__main__":
    camera.run(process_frame)