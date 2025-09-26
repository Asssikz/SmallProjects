from pibody import PushButton, Switch, Touch, Display
from time import sleep

btn_1 = PushButton('A')
btn_2 = PushButton('D')
switch = Switch('B')
touch = Touch('E')


display = Display()
font = display.font_big

result = 0
index = 0
operator = '+'

numbers = [0, 0]

while True:
    if touch.value() == 1:
        index = 1 - index
        sleep(0.1)

    if btn_1.value():
        numbers[index] += 1

    if btn_2.value():
        numbers[index] -= 1
        if numbers[index] < 0:
            numbers[index] = 0

    operator = '+' if switch.value() else '-'

    result = 0
    if operator == '+':
        result = numbers[0] + numbers[1]
    else:
        result = numbers[0] - numbers[1]

    offset_a = len(str(numbers[0])) * 16
    display.text(f"{numbers[0]}", 10, 10, fg=display.GREEN if index == 0 else display.WHITE, font=font)
    display.text(f"{operator}", 10 + offset_a, 10, font=font)
    display.text(f"{numbers[1]}", 10 + offset_a + 16, 10, fg=display.GREEN if index == 1 else display.WHITE, font=font)

    offset_b = len(str(numbers[1])) * 16 + 16 + offset_a
    display.text(f"={result}         ", 10 + offset_b, 10, font=font)

    sleep(0.1)

