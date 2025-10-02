from pibody import LED, Button, Buzzer
from time import sleep

# Define the pin numbers for the LEDs
led_slots = ['A', 'B', 'C'] # green, yellow, red
button_slot = 'E'
buzzer_slot = 'D'

# Initialize the LEDs, button, and buzzer
leds = [LED(pin) for pin in led_slots]
button = Button(button_slot)
buzzer = Buzzer(buzzer_slot)
buzzer.freq(440)  # Set frequency for the buzzer

colors = {
    'green': 0,
    "yellow": 1,
    "red": 2
}

freq_map = {
    'green': 440,  # Frequency for green light
    'yellow': 330,  # Frequency for yellow light
    'red': 220,      # Frequency for red light
    'nothing': 0  # No sound   
}

def beep(freq):
    buzzer.freq(freq_map[freq])  # Set frequency for the buzzer
    buzzer.duty_u16(8192)  # Turn on the buzzer
    sleep(0.1)  # Beep duration
    buzzer.duty_u16(0)  # Turn off the buzzer

def blinking(led):
    for i in range(3):
        leds[colors[led]].on()
        sleep(0.4)
        beep(led)
        leds[colors[led]].off()
        sleep(0.2)

def start_traffic_light():
    sleep(1)

    # LED red
    blinking("red")

    # LED yellow
    beep("yellow")
    leds[colors["yellow"]].on()
    sleep(2)
    leds[colors["yellow"]].off()

    # LED green
    leds[colors["green"]].on()
    beep("green")
    sleep(3.4)
    blinking("green")

    # LEDs off
    for led in leds:
        led.off()
    beep("red")

while True:
    if button.read() == 1:
        start_traffic_light()
    else:
        for i in range(2):
            leds[i].off()
        leds[2].on()
