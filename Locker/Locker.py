from pibody import Encoder, LEDTower, Button, Buzzer, Servo
from time import sleep
from time import ticks_ms
from machine import Pin, PWM

encoder = Encoder('B')
button = Button('A')
servo = Servo(8)
encoder.wrap(0, 7)
buzzer = Buzzer('E')
np = LEDTower(4)

PASSWORD = [3,1,4]
TIMEOUT = 15000
START_ANGLE = 90
TARGET_ANGLE = 125
# NEOPIXEL CONFIG
BRIGHTNESS = 1.0
SELECTED_COLOR = (0, 0, 255)
INPUT_COLOR = (255, 255, 0) 
CORRECT_COLOR = (0, 255, 0)
INCORRECT_COLOR = (255, 0, 0)
SLEEP_COLOR = (20, 40, 120)
BLACK = (0, 0, 0)
# SLEEP_ANIMATION = "RING" 
SLEEP_ANIMATION = "BAR" 


isSleeping = False

def np_show_input(entered, current):
    for i in range(len(np)):
        if i == current:
            np_set_pixel(i, SELECTED_COLOR)
        elif i in entered:
            np_set_pixel(i, INPUT_COLOR)
        else:
            np_set_pixel(i, BLACK)
    np.write()


def np_submit(isCorrect):
    color = CORRECT_COLOR if isCorrect else INCORRECT_COLOR
    for i in range(6):
        for j in range(len(np)):
            submit_color = color if i % 2 == 0 else BLACK
            np_set_pixel(j, submit_color)

        np.write()
        sleep(0.1)


def np_set_colors(colors):
    for i in range(len(np)):
        if i < len(colors):
            np_set_pixel(i, colors[i])
        else:
            np_set_pixel(i, BLACK) 
    np.write()

def np_set_pixel(index, color, brightness=BRIGHTNESS):
    np[index] = tuple(int(c * brightness) for c in color)

def np_reset():
    for i in range(len(np)):
        np[i] = BLACK  # Turn off all LEDs
    np.write() 


def sleep_animation_ring():
    for i in range(len(np)):
        for j in range(len(np)):
            index = (j + i) % len(np)
            brightness = ((j + 1) / len(np)) ** 2 
            np_set_pixel(index, SLEEP_COLOR, brightness)
        if isSleeping == 0:
            return False
        np.write()
        sleep(0.07)
    return True

def sleep_animation_bar():
    for i in range(len(np) * 2 - 1):
        index = abs(len(np) - i - 1)
        for j in range(len(np)):
            distance = abs(j - index) / len(np)
            brightness = (1 - distance) ** 3            
            np_set_pixel(j, SLEEP_COLOR, brightness)
        if isSleeping == 0:
            return False
        np.write()
        sleep(0.07)
    return True

def sleep_reset():
    global isSleeping
    isSleeping = False

def sleep_animation():
    global isSleeping
    isSleeping = True
    if SLEEP_ANIMATION == "BAR":
        animation = sleep_animation_bar
    else:
        animation = sleep_animation_ring

    while animation():
        pass
        

def buzz_submit(isCorrect):
    if isCorrect:
        buzz_sound(2000, 0.1)
    else:
        buzz_sound(200, 0.5)

def buzz_click():
    buzz_sound(64, 0.01)  # Optional: sound for click

def buzz_sound(freq, duration, loudness=1):
    buzzer.freq(freq)
    duty = int(32768 * loudness)  
    buzzer.duty_u16(duty)  
    sleep(duration)  
    buzzer.duty_u16(0)  

isTimeout = 0
last_action_time = ticks_ms()
encoder_value = 0

def set_angle(angle):
    proportion = angle / 180
    pulse_width = proportion * 2 + 0.5
    duty = int(pulse_width * 65535 / 20)
    servo.duty_u16(duty)


set_angle(START_ANGLE) 

old_direction = 0
password_input = []

def input_number(value):
    password_input.append(value)
    if len(password_input) > len(PASSWORD) - 1:
        password_input.pop(0)


def submit(isCorrect):
    encoder._hal_disable_irq()
    if isCorrect:
            buzz_submit(True)
            np_submit(True)
            set_angle(TARGET_ANGLE)
            sleep(3)
            set_angle(START_ANGLE)
    else:
        np_submit(False)
        buzz_submit(False)
        sleep(1)

    encoder.reset()
    encoder._hal_enable_irq()
    np_reset()

def input_handler():
    global old_direction, encoder_value
    
    direction = encoder.direction()
    encoder_value = encoder.value()

    if direction != old_direction and old_direction != 0:
        input_number(encoder.old_value())
    
    np_show_input(password_input, encoder_value)  
    old_direction = direction

def timeout_handler():
    global isTimeout, last_action_time
    if isTimeout == 1:
        np_reset()
    isTimeout = 0
    sleep_reset()
    buzz_click()
    last_action_time = ticks_ms()

def encoder_handler():
    input_handler()
    timeout_handler()
    
    
encoder.add_listener(encoder_handler)  # Update last action time on rotation

while True:
    if button.value():
        password_input.append(encoder_value)
        submit(password_input == PASSWORD)
        password_input.clear()
        
    if (ticks_ms() - last_action_time > TIMEOUT) and isTimeout == 0:
        np_reset()
        encoder.reset()
        set_angle(START_ANGLE)
        isTimeout = 1
        sleep_animation()

