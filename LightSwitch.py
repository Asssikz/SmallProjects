from pibody import Motion, Servo
from time import sleep

servo = Servo(8)
motion = Motion("A")

DEFAULT, ON, OFF = 67, 15, 115
counter = 0
state = "Light is OFF"
servo.angle(DEFAULT)

while True:
    if motion.value():
        if state == "Light is OFF":
            servo.angle(ON)
            sleep(3)
            servo.angle(DEFAULT)
        state = "Light is ON"
        counter = 0

    counter += 1

    if counter > 50:
        if state == "Light is ON":
            servo.angle(OFF)
            sleep(3)
            servo.angle(DEFAULT)
        state = "Light is OFF"
        counter = 0
    
    sleep(0.1)              