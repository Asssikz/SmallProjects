from machine import Pin, PWM, Timer
from time import sleep, sleep_ms, ticks_ms, ticks_diff
from random import randint

green_led = Pin(2, Pin.OUT)
yellow_led = Pin(4, Pin.OUT)
red_led = Pin(6, Pin.OUT)

green_button = Pin(26, Pin.IN)
yellow_button = Pin(18, Pin.IN)
red_button = Pin(16, Pin.IN)

buzzer = PWM(Pin(0, Pin.OUT))

leds = [green_led, yellow_led, red_led]
buttons = [green_button, yellow_button, red_button]

current_pattern = [] 
input_pattern = []

loudness = 100

last_interacted_time = ticks_ms()
replay_time = 20000

timer = Timer()
def get_duty_by_loudness(loudness):
    return int(65535 - (loudness / 100) * 32768)  

def play_button(button_index, duration=0.3):
    global last_interacted_time
    last_interacted_time = ticks_ms()
    turn_off()
    leds[button_index].on()
    buzzer.freq(400 + button_index * 144)  
    buzzer.duty_u16(get_duty_by_loudness(loudness))  
    sleep(duration)
    buzzer.duty_u16(0)

    
def button_handler(pin):
    pin.irq(handler=None)  # Disable the interrupt to prevent re-entrancy

    for i in range(len(buttons)):
        if pin == buttons[i]:
            button_index = i
    input_pattern.append(button_index)    
    


    play_button(button_index)
    sleep(0.3)  # Debounce delay
    pin.irq(trigger=Pin.IRQ_RISING, handler=button_handler)  # Disable the interrupt to prevent re-entrancy


def play_pattern():
    for index in current_pattern:
        play_button(index, duration=0.5)
        leds[index].off()
        sleep(0.2)  # Pause between button presses

    
# for button in buttons:
#     button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

def add_sequence():
    current_pattern.append(randint(0, 2))

def input():
    input_pattern.clear()
    while len(input_pattern) < len(current_pattern):
        for i, button in enumerate(buttons):
            if button.value() == 1:
                input_pattern.append(i)
                if input_pattern != current_pattern[:len(input_pattern)]:
                    print("Wrong pattern!")
                    input_pattern.clear()
                    return False
                play_button(i)
        
        if ticks_diff(ticks_ms(), last_interacted_time) > replay_time:
            print("Time's up! Replay the pattern.")
            play_pattern()
            input_pattern.clear()
    return True

def game_over():
    buzzer.freq(400)
    buzzer.duty_u16(get_duty_by_loudness(loudness))
    for _ in range(6):
        for led in leds:
            led.toggle()
        sleep(0.1)
    buzzer.duty_u16(0)
    print("Your score:", len(current_pattern))


def play_buzzer(frequency, duration=100):
    if frequency < 8:
        buzzer.duty_u16(0)
        sleep_ms(duration)
        return
    buzzer.freq(frequency)
    buzzer.duty_u16(get_duty_by_loudness(loudness))  
    sleep_ms(duration)
    buzzer.duty_u16(0)  

def start_up_meloday():
    play_buzzer(196, 400)
    play_buzzer(233, 400)
    play_buzzer(261, 400)
    play_buzzer(196, 300)
    play_buzzer(174, 300)
    play_buzzer(233, 300)
    play_buzzer(311, 600)
   
led_ind = 0
def circle_leds():
    global led_ind
    led = leds[led_ind]
    led_ind = (led_ind + 1) % len(leds)
    led.toggle()

def start_game():
    timer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: circle_leds())
    start_up_meloday()
    timer.deinit() 

def wait_button_press():
    while True:
        for button in buttons:
            if button.value() == 1:
                return
        sleep(0.1)

def turn_off():
    for led in leds:
        led.off()

turn_off()
start_game()
wait_button_press()
turn_off()

for i in range(3):
    turn_off()
    leds[2-i].on()
    sleep(1)

turn_off()
sleep(0.5)

while True:
    add_sequence()
    play_pattern()

    if input():
        print("Correct pattern!")
    else:
        print("Try again!")
        current_pattern.clear()
        game_over()

    
    sleep(1)



