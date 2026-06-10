import threading
import time

import RPi.GPIO as GPIO

import config


class SortingDetectedObject:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    def __init__(self, pin_led_1: int = config.PIN_LED_1, pin_led_2: int = config.PIN_LED_2, 
                 pin_motor_dc_1: int = config.PIN_MOTOR_DC_1,
                 pin_motor_dc_2: int = config.PIN_MOTOR_DC_2, 
                 motor_dc_power: int = 85,
                 pin_motor_stepper_dir: int = config.PIN_MOTOR_STEPPER_DIR, 
                 pin_motor_stepper_step: int = config.PIN_MOTOR_STEPPER_STEP,
                 motor_stepper_delay: float = 0.005):
        
        self._led_pin1 = pin_led_1
        self._led_pin2 = pin_led_2

        self._motor_dc_pin1 = pin_motor_dc_1
        self._motor_dc_pin2 = pin_motor_dc_2
        self._motor_dc_power = motor_dc_power

        self._motor_stepper_dir = pin_motor_stepper_dir
        self._motor_stepper_step = pin_motor_stepper_step
        self._motor_stepper_delay = motor_stepper_delay

        self._first_detection = False
        self._last_category = None  
        
        self._dc_moving = False 

        GPIO.setup(self._led_pin1, GPIO.OUT)
        GPIO.setup(self._led_pin2, GPIO.OUT)

        GPIO.setup(self._motor_dc_pin1, GPIO.OUT)
        GPIO.setup(self._motor_dc_pin2, GPIO.OUT)
        
        self._pwm_dc1 = GPIO.PWM(self._motor_dc_pin1, 100)
        self._pwm_dc2 = GPIO.PWM(self._motor_dc_pin2, 100)
        self._pwm_dc1.start(0) 
        self._pwm_dc2.start(0) 

        GPIO.setup(self._motor_stepper_dir, GPIO.OUT)
        GPIO.setup(self._motor_stepper_step, GPIO.OUT)
        GPIO.output(self._motor_stepper_dir, GPIO.HIGH)
        
        self._stepper_running = True
        self._stepper_thread = threading.Thread(target=self._run_stepper_motor, daemon=True)
        self._stepper_thread.start()

    def _run_stepper_motor(self):
        delay = self._motor_stepper_delay
        while self._stepper_running:
            GPIO.output(self._motor_stepper_step, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self._motor_stepper_step, GPIO.LOW)
            time.sleep(delay)

    def _run_dc_motor_logic(self, forward: bool):
        self._dc_moving = True  
        
        if not self._first_detection:
            movement_time = 3.5
            self._first_detection = True 
        else:
            movement_time = 7.0

        if forward:
            self._pwm_dc2.ChangeDutyCycle(0)
            self._pwm_dc1.ChangeDutyCycle(self._motor_dc_power)
        else:
            self._pwm_dc1.ChangeDutyCycle(0)
            self._pwm_dc2.ChangeDutyCycle(self._motor_dc_power)

        time.sleep(movement_time)
        
        self._pwm_dc1.ChangeDutyCycle(0)  
        self._pwm_dc2.ChangeDutyCycle(0)  
        
        self._dc_moving = False  

    def sort_object(self, objects_result):
        if self._dc_moving:
            return

        if not objects_result or len(objects_result.boxes) == 0:
            GPIO.output(self._led_pin1, GPIO.LOW)
            GPIO.output(self._led_pin2, GPIO.LOW)
            return
        
        object_name = objects_result.names[int(objects_result.boxes.cls[0])]

        current_category = None
        if object_name in ["pepsi", "cola"]:
            current_category = "pepsi_cola"
        elif object_name in ["fanta", "sprite"]:
            current_category = "fanta_sprite"

        if current_category is None or current_category == self._last_category:
            return

        self._last_category = current_category  

        if current_category == "pepsi_cola":
            GPIO.output(self._led_pin1, GPIO.HIGH)
            GPIO.output(self._led_pin2, GPIO.LOW)
            
            dc_thread = threading.Thread(target=self._run_dc_motor_logic, args=(True,), daemon=True)
            dc_thread.start()
            
        elif current_category == "fanta_sprite":
            GPIO.output(self._led_pin1, GPIO.LOW)
            GPIO.output(self._led_pin2, GPIO.HIGH)
            
            dc_thread = threading.Thread(target=self._run_dc_motor_logic, args=(False,), daemon=True)
            dc_thread.start()

    def cleanup(self):
        self._stepper_running = False
        
        if hasattr(self, '_pwm_dc1'):
            self._pwm_dc1.stop()
        if hasattr(self, '_pwm_dc2'):
            self._pwm_dc2.stop()

        if hasattr(self, '_stepper_thread'):
            self._stepper_thread.join(timeout=0.2)

        GPIO.output(self._led_pin1, GPIO.LOW)
        GPIO.output(self._led_pin2, GPIO.LOW)
        GPIO.output(self._motor_stepper_step, GPIO.LOW)
        GPIO.output(self._motor_stepper_dir, GPIO.LOW)
        GPIO.output(self._motor_dc_pin1, GPIO.LOW)
        GPIO.output(self._motor_dc_pin2, GPIO.LOW)

        GPIO.cleanup()