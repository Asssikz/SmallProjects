from pibody import Distance, Buzzer, LEDTower
from time import sleep

led = LEDTower(18)

buzzer = Buzzer('F')
buzzer.freq(523)

sensor = Distance('C')

while True:
    distance = sensor.read()
    print(distance)

    if distance == 20 or distance == 8190:
        led.fill((0, 100, 0))
        led.write()
        buzzer.duty_u16(0)
        continue

    if 75 <= distance and distance < 150:

        led.fill((100, 100, 0))
        led.write()

        buzzer.duty_u16(16384)
        sleep(0.3)

        led.fill((0, 0, 0))
        led.write()
        buzzer.duty_u16(0)
        sleep(0.05)
        
    elif distance < 75:
        led.fill((100, 0, 0))
        led.write()     
        buzzer.duty_u16(16384)
        sleep(0.2)

        led.fill((0, 0, 0))
        led.write()
        buzzer.duty_u16(0)
        
    else:
        led.fill((0, 100, 0))
        led.write()
        buzzer.duty_u16(0)
        
    sleep(0.1)