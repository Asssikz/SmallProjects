from pibody import GyroAxel, LEDTower
from time import sleep

gyro = GyroAxel("F")
led = LEDTower(4)
num_leds = 8

def show_level(value):
    led_index = int((value + 180) / 360 * (num_leds - 1))
    led.fill((0, 0, 0))

    if abs(value) < 10:
        color = (0, 50, 0)
    else:
        color = (0, 0, 50)

    led[led_index] = color
    led.write()

while True:
    x, y, z = gyro.read_accel_data()
    y = y * 180
    show_level(y)
    sleep(0.1)
