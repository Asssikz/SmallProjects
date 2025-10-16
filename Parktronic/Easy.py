from pibody import Distance, LEDTower
from time import sleep

led = LEDTower(18)
sensor = Distance('C')

while True:
    distance = sensor.read()
    print(distance)

    if distance in (0, 20, 8190):
        continue

    distance = min(300, max(50, distance))
    index = round(((distance - 50) / 250) * 7)

    for i in range(8):
        if i <= index:
            led[i] = (0, 50, 0) 
        else: 
            led[i] = (0, 0, 0)
    led.write()
    sleep(0.1)