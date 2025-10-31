from pibody import LED, Button, Buzzer
from random import randint
from time import sleep

green_led = LED("B")
yellow_led = LED("D")
red_led = LED("E")

green_button = Button("F")
yellow_button = Button("H")
red_button = Button("G")

buzzer = Buzzer("A")
buzzer.volume(0.5)
buzzer.off()

freq_map = [400, 550, 700]

leds = [green_led, yellow_led, red_led]
buttons = [green_button, yellow_button, red_button]

def show_sequence():
    for i in actual_sequence:
        leds[i].on()
        buzzer.freq(freq_map[i])
        buzzer.on()
        sleep(0.05)
        buzzer.off()
        sleep(0.75)
        leds[i].off()
        sleep(0.2)

def new_sequence():
    actual_sequence.clear()
    for _ in range(3):
        actual_sequence.append(randint(0, 2))

def check_button(buttons):
    for btn in buttons:
        if btn.value() == 1:
            return True
    return False

def game_over():
    for _ in range(3):
        for led in leds:
            led.on()
        buzzer.beep()
        sleep(0.1)
        for led in leds:
            led.off()
        buzzer.boop()
        sleep(0.1)

def success():
    for led in leds:
        led.on()
    buzzer.freq(1000)
    buzzer.on()
    sleep(0.1)
    buzzer.off()
    sleep(0.1)
    buzzer.freq(1500)
    buzzer.on()
    sleep(0.1)
    buzzer.off()
    for led in leds:
        led.off()
    sleep(0.1)

actual_sequence = []
button_sequence = []

# Waiting of start game
def waiting_for_start():
    for led in leds:
        led.on()
    while not check_button(buttons):
        sleep(0.1)
    for led in leds:
        led.off()

game_status = 'waiting'
while True:
    if game_status == 'waiting':
        waiting_for_start()
        game_status = 'playing'
        sleep(0.5)
        new_sequence()
        show_sequence()

    # Zone of buttons pressing
    while len(button_sequence) < len(actual_sequence):
        for btn in buttons:
            if btn.value():
                index = buttons.index(btn)
                button_sequence.append(index)
                leds[index].on()
                buzzer.freq(freq_map[index])
                buzzer.on()
                sleep(0.05)
                buzzer.off()
                print(button_sequence)
                while btn.value():
                    sleep(0.1)
                leds[index].off()

        for i in range(len(button_sequence)):
            if button_sequence[i] != actual_sequence[i]:
                game_status = 'lose'

        if game_status == 'lose':
            break

    button_sequence.clear()
    if game_status == 'playing':
        sleep(0.2)
        success()
        sleep(0.4)
        actual_sequence.append(randint(0, 2))
        show_sequence()
        sleep(0.3)
        
    if game_status == 'lose':
        game_status = 'waiting'
        game_over()
        sleep(0.5)