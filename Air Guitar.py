from pibody import Buzzer, Button, GyroAxel
from time import sleep

sensor = GyroAxel('D')
btn = Button('E')
buzzer = Buzzer('C')

NOTES_MATRIX = [
    #   C     D     E     F     G     A     B
    [ 262,  294,  330,  349,  392,  440,  494],  # 4 октава
    [ 523,  587,  659,  698,  784,  880,  988],  # 5 октава
    [1047, 1175, 1319, 1397, 1568, 1760, 1976],  # 6 октава
]

while True:
    ax, ay, az = sensor.read_accel()
    x = min(1.0, max(-1.0, round(ax, 1)))
    y = min(1.0, max(-1.0, round(ay, 1)))

    note_index = round(x * 3) + 3
    octave = round(y + 1)
    
    freq = NOTES_MATRIX[octave][note_index]
    buzzer.freq(freq)

    if btn.value() == 1:
        buzzer.volume(0.5)
    else:
        buzzer.volume(0.0)

    sleep(0.1)