from pibody import LEDTower, Sound
from time import sleep, ticks_ms

sensor = Sound('C')
led = LEDTower()

status = 0
last_trig = 0

while True:
    aSignal = sensor.read_analog()
    difference = abs(0.5 - aSignal)
    print(difference)

    if abs(0.5 - sensor.read_analog()) > 0.04:
        last_trig = ticks_ms()
        if abs(0.5 - sensor.read_analog()) > 0.04 and ticks_ms() - last_trig < 150 and ticks_ms() - last_trig > 50:
            status = 1 - status

    led.fill((status*50,)*3)
    led.write()

    sleep(0.1)