from pibody import LED, Button, Buzzer
from time import sleep

ledG = LED("D")
ledY = LED("B")
ledR = LED("A")
leds = [ledG, ledY, ledR]

btn = Button("F")
buz = Buzzer("C")

def blinking(led):
    for _ in range(3):
        led.on()
        sleep(0.3)
        buz.beep()
        led.off()
        sleep(0.2)

while True:
    if btn.value() == 1:
        for led in leds:
            led.on()
            sleep(2)
            blinking(led)
            led.off()
    else:
        ledG.on()
        for led in leds[1:]:
            led.off()