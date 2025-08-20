from pibody import Display, PushButton, LEDTower
from time import sleep, ticks_ms

display = Display()
next_btn = PushButton("A")
enter_btn = PushButton("D")
led_tower = LEDTower()

num_of_bits = 8

index = num_of_bits - 1
binary = [0] * num_of_bits

last_next, last_enter, last_blink = 0, 0, 0
blinking = False

display.text("Binary: ", 10, 10)
display.text("Decimal:", 10, 26)

while True:
    now = ticks_ms()

    # Next button
    if next_btn.value() and now - last_next > 200:
        last_next = now
        index -= 1
        if index < 0:
            index = num_of_bits - 1

    # Enter button
    if enter_btn.value() and now - last_enter > 200:
        last_enter = now
        binary[index] = 1 - binary[index]

    # LED tower update
    for i, bit in enumerate(binary):
        led_tower[i] = (255, 255, 255) if bit else (0, 0, 0)

    # Blinking selected LED
    if now - last_blink > 350:
        last_blink, blinking = now, not blinking
    led_tower[index] = (50, 50, 50) if blinking else (binary[index] * 255,) * 3
    led_tower.write()

    # Display numbers
    for i, bit in enumerate(binary):
        color = display.GREEN if i == index else display.WHITE
        display.text(str(bit), 74 + i*8, 10, fg=color)

    decimal = int("".join(map(str, binary)), 2)
    display.text(f"{decimal}     ", 82, 26)

    sleep(0.1)