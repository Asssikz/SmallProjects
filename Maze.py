from pibody import Servo, Joystick

servoX = Servo(8)
servoY = Servo(9)
joystick = Joystick('F')

servoX.angle(90)
servoY.angle(90)

while True:
    x, y = joystick.read()
    angleX = round((1-x) * 30 + 75)
    angleY = round(y * 30 + 75)

    servoX.angle(angleX)
    servoY.angle(angleY)