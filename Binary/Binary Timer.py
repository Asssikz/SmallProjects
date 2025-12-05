from pibody import Encoder, LEDTower, Button, Buzzer
from time import ticks_ms, ticks_diff, sleep

buzzer = Buzzer('F')
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

def finish():
    for _ in range(3):
        led.fill((50, 50, 0))
        led.write()
        buzzer.make_sound(1000, 0.3, 0.1)
        sleep(0.1)
        led.fill((0, 0, 0))
        led.write()
        sleep(0.1)

while True:
    if button.read():
        while button.read():
            sleep(0.1)
        state = 1 - state if value > 0 else 0

    if state == 0:
        value = encoder.value()

    if state == 1 and ticks_diff(ticks_ms(), last_time) > 1000:
        last_time = ticks_ms()
        value -= 1
        buzzer.make_sound(220, 0.3, 0.05)
        encoder.set_value(value)
        state = 0 if value == 0 else 1
        
        sleep(0.1)
        if state == 0:
            finish()

    update_binary(value)
    update_led()