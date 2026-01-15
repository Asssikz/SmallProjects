from pibody import LED, Button, Buzzer
from time import sleep

ledR = LED("A")
ledY = LED("B")
ledG = LED("C")
leds = [ledG, ledY, ledR]
freqs = [440, 330, 220]

buz = Buzzer("D")
btn = Button("E")

def blinking(led, index):
    for _ in range(3):
        led.on()
        sleep(0.3)
        buz.make_sound(freqs[index], 1, 0.1)
        led.off()
        sleep(0.2)

while True:
    if btn.value() == 1:
        for i, led in enumerate(leds):
            led.on()
            sleep(2)
            blinking(led, i)
            led.off()
    else:
        ledG.on()
        for led in leds[1:]:
            led.off()