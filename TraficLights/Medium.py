from pibody import LED, Button
from time import sleep

ledG = LED("D")
ledY = LED("B")
ledR = LED("A")
leds = [ledG, ledY, ledR]

btn = Button("F")

while True:
    if btn.value() == 1:
        for led in leds:
            led.on()
            sleep(2)
            led.off()
    else:
        ledG.on()
        for led in leds[1:]:
            led.off()