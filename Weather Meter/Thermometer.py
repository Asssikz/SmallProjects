from pibody import Climate, LEDTower
from time import sleep

sensor = Climate("A")
tower = LEDTower()

while True:
    temp = sensor.read_temperature()
    temp = max(min(temp, 30), 20)

    index = int(((temp - 20) / 10) * 8)

    for i in range(8):
        if i <= index:
            tower[i] = (0, 50, 0)
        else:
            tower[i] = (0, 0, 0)
    tower.write()
    sleep(0.1)