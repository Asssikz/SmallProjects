from pibody import Distance, Buzzer, LEDTower
from time import sleep

led = LEDTower(18)

buzzer = Buzzer('F')
buzzer.freq(523)

sensor = Distance('C')

def danger():
    for i in range(2):
        buzzer.volume(0.25 * (1 - i))
        led.fill((50 * (1 - i), 0, 0))
        led.write()
        sleep(0.1)

def get_color(distance):
    if distance < 120:
        return (80, 0, 0) 
    elif distance < 190:
        return (80, 50, 0)
    else:
        return (0, 80, 0)

while True:
    distance = sensor.read()
    print(distance)

    if distance == 20 or distance == 8190 or distance == 0:
        buzzer.duty_u16(0)
        continue

    if distance < 50:
        danger()
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
