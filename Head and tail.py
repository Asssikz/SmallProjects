from pibody import Button, LED, display
from time import sleep
from random import randint

button = Button('A')
led1 = LED('D')
led2 = LED('E')
coin = 0

while True:
    if button.value(): 
        coin = randint(1, 2)
        if coin == 1:
            display.print("Heads")
            led1.on()
            led2.off()
        else:
            display.print("Tails")
            led2.on()
            led1.off()
        sleep(0.3)
