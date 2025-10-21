from pibody import PWM, Motion, Light
import time

led = PWM('A')
motion = Motion('B')
light = Light('C')

light_treshold = 37500  # максимальное значение для светодиода
dim_brightness = 2500   # начальная яркость светодиода
full_brightness = 35000 # максимальная яркость светодиода

def fade_to(brightness, led, step=1000, delay=0.01):
    current = led.duty()
    if brightness > current:
        for i in range(current, brightness, step):
            led.duty(i / 65535)
            time.sleep(delay)
    else:
        for i in range(current, brightness, -step):
            led.duty(i / 65535)
            time.sleep(delay)
    led.duty(brightness / 65535)

while True:
    light_value = light.read() * 65535
    motion_value = motion.read()

    if light_value > light_treshold:
        fade_to(0, led)
        continue

    if motion_value == 1:
        fade_to(full_brightness, led)
    else:
        fade_to(dim_brightness, led)
