import os

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

from pathlib import Path
import time
from typing import Callable

import cv2
from cv2.typing import MatLike
import numpy as np
from ultralytics import YOLO

import config


class Camera:
    def __init__(self, camera_id: int = config.CAMERA_ID, width: int = config.CAMERA_WIDTH, height: int = config.CAMERA_HEIGHT):
        self.camera_id = camera_id
        self.width = width
        self.height = height

        self.last_reconnect_time = 0
        self.connected = False
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        self.__window_name = "Bottle Sorting System"
        
        self.__initialize_capture()

    def __initialize_capture(self):
        self.capture = cv2.VideoCapture(self.camera_id)
        if self.capture.isOpened():
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
            self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1) 
            
            self.connected = True
        else:
            self.capture = None
            self.connected = False

    def read_frame(self) -> MatLike:
        ret = False

        if self.capture and self.capture.isOpened():
            ret, frame_raw = self.capture.read()
            if ret:
                self.frame = frame_raw
                self.connected = True
                return self.frame

        self.connected = False
        current_time = time.time()
        
        if current_time - self.last_reconnect_time > 2.0:
            if self.capture:
                self.capture.release()
            self.__initialize_capture()
            self.last_reconnect_time = current_time 
        
        error_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        msg = "CAMERA NOT FOUND!"
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(msg, font, 1.2, 3)[0]
        text_x = (self.width - text_size[0]) // 2
        text_y = (self.height + text_size[1]) // 2
        
        cv2.putText(error_frame, msg, (text_x, text_y), font, 1.2, (0, 0, 255), 3)
        self.frame = error_frame
        return self.frame

    def run(self, process_frame: Callable[[], MatLike]):
        cv2.namedWindow(self.__window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.__window_name, self.width, self.height)

        prev_time = time.time()
        frames_passed = 0
        fps_real = 0.0
        
        while True:
            self.frame = process_frame()

            frames_passed += 1
            current_time = time.time()
            if current_time - prev_time >= 1.0:
                fps_real = frames_passed / (current_time - prev_time)
                frames_passed = 0
                prev_time = current_time

            cv2.putText(self.frame, f"FPS: {int(fps_real)}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(self.__window_name, self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if self.capture:
                    self.capture.release()
                cv2.destroyAllWindows()
                break  
 

class Detection:
    def __init__(self, model_path: str | Path = config.MODEL_PATH, confidence: float = config.CONFIDENCE_THRESHOLD):
        self.model = YOLO(str(model_path))
        self.confidence = confidence
        self.result = None

        self.classes = self.model.names


    def get_detected_objects(self, frame: MatLike):
        self.result = self.model.track(source = frame,
                                  verbose = False,
                                  conf = self.confidence,
                                  iou = 0.35)[0]
        
    def draw_detected_objects(self, frame: MatLike):
        
        if self.result and self.result.boxes and len(self.result.boxes) > 0:
            class_names = self.result.names

            for box in self.result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                x_mid = (x1 + x2) // 2
                y_mid = (y1 + y2) // 2

                cls = int(box.cls[0])
                class_name = class_names[cls]

                conf = float(box.conf[0])

                colour = config.OBJECTS_COLOUR.get(class_name, (255, 255, 255))

                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                cv2.circle(frame, (x_mid, y_mid), 3, colour, 1)

                cv2.putText(frame, 
                            f"{class_name} {conf:.2f}",
                            (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, colour, 2)
