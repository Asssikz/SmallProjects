from pibody import LEDTower, Buzzer, Distance, Button

led_tower = LEDTower("H")
buzzer = Buzzer("F")
distance = Distance("C")
button1 = Button("B")
button2 = Button("E")

notes = [
    261,
    294,
    330,
    349,
    392,
    440,
    494,
    523
]

while True:
    key = (distance.read() - 30) // 9
    key = max(min(key, 7), 0)

    led_tower.fill((50, 50, 50))
    led_tower[key] = (0, 50, 50)
    led_tower.write()

    buzzer.freq(notes[key])
    buzzer.volume(button1.read() | button2.read())