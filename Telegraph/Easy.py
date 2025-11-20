from pibody import Button, Buzzer, LED
from time import sleep

buz = Buzzer('A')
buz.freq(800)
led = LED('B')
btn = Button('D')

while True:
    if btn.value():
        led.on()
        buz.volume(0.2)
    else:
        led.off()
        buz.volume(0.0)
    sleep(0.1)