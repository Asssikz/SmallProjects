from pibody import Encoder, Button, display

encoder = Encoder('C')
button = Button('A')

while True:
    if button.read():
        encoder.set_value(0)
        value = 0
        while button.read():
            continue
    
    value = abs(encoder.value())
    display.text(f"sm: {round(value/4.5,1)}   ", 10, 10)