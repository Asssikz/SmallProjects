from pibody import Distance, LEDTower
from time import sleep

led = LEDTower(18)
sensor = Distance('C')

def get_color(distance):
    if distance < 70:
        return (80, 0, 0)
    elif distance < 150:
        return (80, 50, 0)
    else:
        return (0, 80, 0)

while True:
    distance = sensor.read()
    print(distance)

    if distance in (0, 20, 8190):
        continue

    distance = min(300, max(50, distance))
    index = round(((distance - 50) / 250) * 7)
    color = get_color(distance)

    for i in range(8):
        if i <= index:
            led[i] = color
        else: 
            led[i] = (0, 0, 0)
    led.write()
    sleep(0.1)