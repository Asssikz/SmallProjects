from pibody import Encoder, LEDTower, Button
from time import ticks_ms, ticks_diff, sleep

button = Button('E')

encoder = Encoder('G')
encoder.wrap(0, 255)
led = LEDTower(18)
binary = [0] * 8

state = 0
last_time = 0
value = 0

def update_binary(value):
    for i in range(8):
        binary[i] = (value // (2 ** (7 - i))) % 2

def update_led():
    for i in range(8):
        if binary[i] == 1:
            led[i] = (50, 50, 50)
        else:
            led[i] = (0, 0, 0)
    led.write()

while True:
    if button.read():
        while button.read():
            sleep(0.1)
        state = 1 - state if value > 0 else 0

    if state == 0:
        value = encoder.value()
        update_binary(value)
        update_led()

    if state == 1 and value > 0 and ticks_diff(ticks_ms(), last_time) > 1000:
        last_time = ticks_ms()
        value -= 1
        encoder.set_value(value)
        update_binary(value)
        update_led()
        state = 0 if value == 0 else 1
