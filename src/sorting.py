import RPi.GPIO as GPIO


class SortingDetectedObject:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    def __init__(self, led_pin1: int, led_pin2: int):
        self.led_pin1 = led_pin1
        self.led_pin2 = led_pin2
        GPIO.setup(self.led_pin1, GPIO.OUT)
        GPIO.setup(self.led_pin2, GPIO.OUT)

    def sort_object(self, objects_result):
        if not objects_result or len(objects_result.boxes) == 0:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.LOW)
            return
        
        object_name = objects_result.names[int(objects_result.boxes.cls[0])]

        if object_name in ["pepsi", "cola"]:
            GPIO.output(self.led_pin1, GPIO.HIGH)
            GPIO.output(self.led_pin2, GPIO.LOW)
            
        elif object_name in ["fanta", "sprite"]:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.HIGH)
            
        else:
            GPIO.output(self.led_pin1, GPIO.LOW)
            GPIO.output(self.led_pin2, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.led_pin1, GPIO.LOW)
        GPIO.output(self.led_pin2, GPIO.LOW)
        GPIO.cleanup()