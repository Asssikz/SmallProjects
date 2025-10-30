from pibody import Servo, Joystick, Button
import time

servoX = Servo(8)
servoY = Servo(9)
button = Button('B')
joystick = Joystick('F')
state = 0

while True:
    if button.read():
        state = 1 - state
        while button.read():
            time.sleep(0.1)
            
    if state == 0:
        servoX.angle(90)
        servoY.angle(90)
        continue

    x, y = joystick.read()
    angleX = round((1-x) * 30 + 75)
    angleY = round(y * 30 + 75)

    servoX.angle(angleX)
    servoY.angle(angleY)