from pibody import LED, Button, Buzzer, Servo
from time import sleep
from random import randint

led_1p = LED('B')
led_2p = LED('D')

btn_1p = Button('A')
btn_2p = Button('E')

buzzer = Buzzer('C')

servo1 = Servo(8)
servo2 = Servo(9)

servo1.angle(90)
servo2.angle(90)

game_state = 'waiting'
time_limit = 3

def blink_led(led, times = 3, duration = 0.5):
    for i in range(times):
        led.on()
        sleep(duration / 2)
        led.off()
        sleep(duration / 2)

while True:
    print('Press both buttons to start')

    while game_state == 'waiting':
        pressed_1p = btn_1p.value()
        pressed_2p = btn_2p.value()
        if pressed_1p or pressed_2p:
            led_1p.value(pressed_1p) 
            led_2p.value(pressed_2p)
            if pressed_1p and pressed_2p:
                print("Realease both buttons to start")
                while btn_1p.value() or btn_2p.value():
                    sleep(0.1)
                game_state = 'playing'
                print('Game started')
        else:
            led_1p.off()
            led_2p.off()
    
    led_1p.off()
    led_2p.off()
    servo1.angle(90)
    servo2.angle(90)


    time_limit = randint(300, 700)
    # False start check
    for i in range(time_limit):
        if btn_1p.value():
            print('False start! Player 1 loses')
            servo1.angle(180)
            blink_led(led_2p)
            game_state = 'waiting'
            break
        if btn_2p.value():
            print('False start! Player 2 loses')
            servo2.angle(0)
            blink_led(led_1p)
            game_state = 'waiting'
            break
        sleep(0.01)
    else:
        buzzer.beep()

    while game_state == 'playing':
        if btn_1p.value():
            print('Player 1 wins!')
            servo2.angle(0)
            blink_led(led_1p)
            game_state = 'waiting'
            break
        if btn_2p.value():
            print('Player 2 wins!')
            servo1.angle(180)
            blink_led(led_2p)
            game_state = 'waiting'
            break
        sleep(0.01)

