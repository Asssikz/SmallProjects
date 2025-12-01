from pibody import Joystick

joystick = Joystick('F')

password = [1, 1, 3]
input_password = []
treshold = 0.25
center = 0.5

while True:
    x, y = joystick.read()

    direction = None

    if x > center + treshold: # right
        direction = 3
        while x > center + treshold:
            x, y = joystick.read()

    elif x < center - treshold: # left
        direction = 1
        while x < center - treshold:
            x, y = joystick.read()

    elif y > center + treshold: # up
        direction = 2
        while y > center + treshold:
            x, y = joystick.read()

    elif y < center - treshold: # down
        direction = 4
        while y < center - treshold:
            x, y = joystick.read()

    if direction is not None:
        input_password.append(direction)
        print(input_password)

        if len(input_password) == len(password):
            if input_password == password:
                print("Password is correct")
            else:
                print("Password is incorrect")

            input_password.clear()
