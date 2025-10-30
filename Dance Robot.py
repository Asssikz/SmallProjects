'''
    Попытка сделать код, который будет двигать сервопривод под такт музыки. Идеально не получилось, однако я сделал имитацию
        движения при достижение определенного уровня громкости.
'''

from pibody import Servo, Sound
from time import ticks_ms

servo = Servo(8)
sensor = Sound('C')

CENTER = 0.5      # Среднее значение при тишине
SCALE = 180       # Масштаб для перевода отклонений в угол (0–180)
status = -1
now = 0 
angle=90

servo.angle(90)

while True:
    data = sensor.read_analog()  # Значение от 0.0 до 1.0
    deviation = abs(data - CENTER)    # Отклонение от центра (-0.5 до +0.5)

    # Преобразуем отклонение в диапазон углов
    if ticks_ms() - now > 135 and deviation > 0.075:
        now = ticks_ms()
        angle = int(90 + deviation * SCALE * status)  # 90° — середина
        status = status * (-1)
    elif ticks_ms() - now > 135:
        now = ticks_ms()
        angle = 90

    servo.angle(angle)