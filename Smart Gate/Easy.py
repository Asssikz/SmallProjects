from pibody import Servo
from time import sleep

# --- Настройки сервопривода ---
servo = Servo(8)

OPEN_ANGLE = 90   # угол открытия ворот
CLOSE_ANGLE = 0   # угол закрытия ворот
OPEN_TIME_S = 3   # время, на которое ворота открываются

while True:
    print("Открываем ворота...")
    servo.angle(OPEN_ANGLE)
    sleep(OPEN_TIME_S)

    print("Закрываем ворота...")
    servo.angle(CLOSE_ANGLE)
    sleep(OPEN_TIME_S)