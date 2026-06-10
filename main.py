from src.detector import Camera, Detection
from src.sorting import SortingDetectedObject

camera = Camera()
detector = Detection()
sorting_detected_objects = SortingDetectedObject()

frame_counter = 0

def process_frame():
    global frame_counter
    
    frame = camera.read_frame()
    
    if not camera.connected:
        return frame

    if frame_counter % 5 == 0:
        detector.get_detected_objects(frame)
        frame_counter = 0

    if detector.result:
        detector.draw_detected_objects(frame)
        sorting_detected_objects.sort_object(detector.result)
        
    frame_counter += 1
    
    return frame

if __name__ == "__main__":
    try:
        camera.run(process_frame)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sorting_detected_objects.cleanup()