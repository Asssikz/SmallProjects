from pibody import LED, Button
from random import randint
from time import sleep

green_led = LED("A")
yellow_led = LED("B")
red_led = LED("C")

green_button = Button("D")
yellow_button = Button("E")
red_button = Button("F")

leds = [green_led, yellow_led, red_led]
buttons = [green_button, yellow_button, red_button]

actual_sequence = []
button_sequence = []


def new_sequence():
    actual_sequence.clear()
    for _ in range(3):
        actual_sequence.append(randint(0, 2))
    print("New sequence:", actual_sequence)


def show_sequence():
    for i in actual_sequence:
        leds[i].on()
        sleep(0.5)
        leds[i].off()
        sleep(0.2)


def read_buttons():
    button_sequence.clear()
    while len(button_sequence) < len(actual_sequence):
        for btn in buttons:
            if btn.value():
                index = buttons.index(btn)
                button_sequence.append(index)
                print("Input:", button_sequence)

                leds[index].on()
                sleep(0.2)
                while btn.value():
                    sleep(0.05)
                leds[index].off()


def check_result():
    for i in range(len(actual_sequence)):
        if actual_sequence[i] != button_sequence[i]:
            return False
    return True


def success():
    # плавная «волна» по светодиодам
    for led in leds:
        led.on()
        sleep(0.1)
        led.off()
    sleep(0.2)


def game_over():
    # три быстрых мигания всеми светодиодами
    for _ in range(3):
        for led in leds:
            led.on()
        sleep(0.1)
        for led in leds:
            led.off()
        sleep(0.1)


while True:
    new_sequence()
    show_sequence()
    read_buttons()

    if check_result():
        success()
    else:
        game_over()

    sleep(0.5)
