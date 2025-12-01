from pibody import LEDTower
from time import sleep

led = LEDTower("A")

MAX_BRIGHTNESS = 150   # максимум яркости (0–255)
MIN_BRIGHTNESS = 10
STEP = 2              # шаг изменения яркости
DELAY = 0.02          # пауза между шагами, влияет на скорость "дыхания"

while True:
    # Плавное включение (вдох)
    for b in range(MIN_BRIGHTNESS, MAX_BRIGHTNESS + 1, STEP):
        led.fill((0, b, b))   # зелёный цвет с яркостью b
        led.write()
        sleep(DELAY)

    # Плавное выключение (выдох)
    for b in range(MAX_BRIGHTNESS, MIN_BRIGHTNESS-1, -STEP):
        led.fill((0, b, b))
        led.write()
        sleep(DELAY)
