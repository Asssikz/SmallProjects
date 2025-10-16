from pibody import Distance, Buzzer, LEDTower
from time import sleep

led = LEDTower(18)
buzzer = Buzzer('F')
buzzer.freq(523)
sensor = Distance('C')

def get_color(distance):
    if distance < 70:
        return (80, 0, 0)
    elif distance < 150:
        return (80, 50, 0)
    else:
        return (0, 80, 0)

def danger_alert():
    for i in range(2):
        buzzer.volume(0.25 * (1 - i))
        led.fill((80 * (1 - i), 0, 0))
        led.write()
        sleep(0.1)

while True:
    distance = sensor.read()
    print(distance)

    if distance in (0, 20, 8190):
        buzzer.duty_u16(0)
        continue

    if distance < 50:
        danger_alert()
        continue

    distance = min(300, max(50, distance))
    index = round(((distance - 50) / 250) * 7)
    color = get_color(distance)

    for i in range(8):
        if i <= index:
            led[i] = (0, 80, 0)
        else:
            led[i] = (0, 0, 0)
    led.write()