from pibody import LED, Distance, Buzzer
from time import sleep

led_yellow = LED('A')
led_red = LED('B')

buzzer = Buzzer('C')
buzzer.freq(523)

sensor = Distance('F')

while True:
    distance = sensor.read()
    print(distance)

    if distance == 20 or distance == 8190:
        led_yellow.off()
        led_red.off()
        buzzer.duty_u16(0)
        continue

    if 40 <= distance and distance < 70:
        
        led_yellow.on()
        led_red.off()
        
        buzzer.duty_u16(16384)
        sleep(0.3)
        buzzer.duty_u16(0)
        sleep(0.05)
        
    elif distance < 40:
        
        led_yellow.on()
        led_red.on()
        
        buzzer.duty_u16(16384)
        sleep(0.2)
        buzzer.duty_u16(0)
        
    else:
        led_yellow.off()
        led_red.off()
        buzzer.duty_u16(0)
        
    sleep(0.1)