from pibody import LED, Button, Buzzer
from time import sleep
from random import randint

# Simple setup: three LEDs, three buttons, one buzzer
green_led = LED("B")
yellow_led = LED("D")
red_led = LED("E")

green_button = Button("F")
yellow_button = Button("H")
red_button = Button("G")

buzzer = Buzzer("A")

leds = [green_led, yellow_led, red_led]
buttons = [green_button, yellow_button, red_button]


def all_leds_off():
    for led in leds:
        led.off()


def play_note(index, duration=0.4):
    leds[index].on()
    buzzer.freq(400 + index * 150)
    buzzer.volume(0.5)
    sleep(duration)
    buzzer.volume(0)
    leds[index].off()
    sleep(0.1)


def show_pattern(pattern):
    for index in pattern:
        play_note(index)


def wait_for_button():
    while True:
        for i, btn in enumerate(buttons):
            if btn.value() == 1:
                while btn.value() == 1:
                    sleep(0.05)
                return i
        sleep(0.05)


def read_player(pattern):
    position = 0
    while position < len(pattern):
        pressed = wait_for_button()
        play_note(pressed, duration=0.25)
        if pressed != pattern[position]:
            return False
        position += 1
    return True


def game_over_feedback(score):
    print("Game over! Score:", score)
    for _ in range(3):
        for led in leds:
            led.on()
        buzzer.freq(250)
        buzzer.volume(0.2)
        sleep(0.25)
        buzzer.volume(0)
        all_leds_off()
        sleep(0.25)


# Main game loop: remember the pattern and repeat it
all_leds_off()
pattern = []

while True:
    pattern.append(randint(0, 2))
    show_pattern(pattern)

    if not read_player(pattern):
        game_over_feedback(len(pattern) - 1)
        pattern = []
        sleep(1)
