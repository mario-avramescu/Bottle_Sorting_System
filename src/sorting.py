import time

import RPi.GPIO as GPIO


class SortingDetectedObject:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    def __init__(self, led_pin1: int, led_pin2: int, servo_pin: int):
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        self.servo_pin = servo_pin

        GPIO.setup(self.led_pin1, GPIO.OUT)
        GPIO.setup(self.led_pin2, GPIO.OUT)

        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)
        self.pwm.start(0)

        self.current_state = "neutral"
        self._set_servo_position("neutral")

    def _set_servo_position(self, position: str):
        if position == "neutral":
            duty = 7.5
        elif position == "left":
            duty = 5.0
        elif position == "right":
            duty = 10.0
        else:
            return
        
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.3)
        self.pwm.ChangeDutyCycle(0)
        

    def sort_object(self, objects_result):
        if not objects_result or len(objects_result.boxes) == 0:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.LOW)
            return
        
        object_name = objects_result.names[int(objects_result.boxes.cls[0])]

        if object_name in ["pepsi", "cola"]:
            GPIO.output(self.led_pin1, GPIO.HIGH)
            GPIO.output(self.led_pin2, GPIO.LOW)

            if self.current_state != "left":
                self._set_servo_position("left")
                self.current_state = "left"
            
        elif object_name in ["fanta", "sprite"]:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.HIGH)

            if self.current_state != "right":
                self._set_servo_position("right")
                self.current_state = "right"
            
        else:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.led_pin1, GPIO.LOW)
        GPIO.output(self.led_pin2, GPIO.LOW)

        self._set_servo_position("neutral") 

        if hasattr(self, 'pwm'):
            self.pwm.stop()
            time.sleep(0.1)
            del self.pwm
        GPIO.cleanup()