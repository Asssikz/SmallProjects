from pibody import LED
from time import sleep

ledG = LED("D")
ledY = LED("B")
ledR = LED("A")
leds = [ledG, ledY, ledR]

while True:
    for led in leds:
        led.on()
        sleep(2)
        led.off()

