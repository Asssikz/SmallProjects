from pibody import LED, Button, Switch

led = LED("A")
button1 = Button("B")
button2 = Button("C")
switch = Switch("D")

while True:
    if switch.value():
        if button1.value() and button2.value():
            led.on()
        else:
            led.off()
    else:
        if button1.value() or button2.value():
            led.on()
        else:
            led.off()