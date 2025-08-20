from pibody import LED, PushButton, Buzzer
from time import sleep

led_1p = LED('A')
led_2p = LED('D')

btn_1p = PushButton('B')
btn_2p = PushButton('E')

buzzer = Buzzer('F')

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

    # False start check
    for i in range(time_limit * 100):
        if btn_1p.value():
            print('False start! Player 1 loses')
            blink_led(led_2p)
            game_state = 'waiting'
            break
        if btn_2p.value():
            print('False start! Player 2 loses')
            blink_led(led_1p)
            game_state = 'waiting'
            break
        sleep(0.01)
    else:
        buzzer.beep()

    while game_state == 'playing':
        if btn_1p.value():
            print('Player 1 wins!')
            blink_led(led_1p)
            game_state = 'waiting'
            break
        if btn_2p.value():
            print('Player 2 wins!')
            blink_led(led_2p)
            game_state = 'waiting'
            break
        sleep(0.01)

