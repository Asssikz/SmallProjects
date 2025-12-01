from pibody import GyroAccel, LED, Buzzer, display
import time

# ---------------- Настройка модулей ----------------

# Порог наклона по оси X
treshold = 0.5

# Индексы и таймер
led_index = 0
last_index = 0
last_time = 0

# Светодиоды (A, B, C)
led_r = LED("A")
led_y = LED("B")
led_g = LED("C")
leds = [led_r, led_y, led_g]

# Датчик ускорения (E)
gyro_accel = GyroAccel("E")

# Пищалка (D)
buzzer = Buzzer("D")
buzzer.volume(0.5)
buzzer.off()

# ---------------- Цвета и координаты для дисплея ----------------

red_color = display.color(255, 0, 0)
yellow_color = display.color(255, 255, 0)
green_color = display.color(0, 255, 0)
dim_red_color = display.color(100, 0, 0)
dim_yellow_color = display.color(100, 100, 0)
dim_green_color = display.color(0, 100, 0)
color_map = [red_color, yellow_color, green_color]
dim_color_map = [dim_red_color, dim_yellow_color, dim_green_color]

x = 20
y = 30
r = 10

# ---------------- Частоты для каждого светодиода ----------------

freq_map = {
    0: 440,  # A4
    1: 330,  # E4
    2: 220,  # C4
}

# ---------------- Вспомогательные функции ----------------

def beep(buzzer, freq, duration=0.05):
    buzzer.freq(freq)
    buzzer.on()
    time.sleep(duration)
    buzzer.off()

def change_index(index, change):
    index += change
    index = min(max(index, 0), len(freq_map) - 1)
    return index

def update_leds(leds, index):
    for i in range(len(leds)):
        if i == index:
            leds[i].on()
            display.fill_circle(x, y + i * 22, r, color_map[i])
        else:
            leds[i].off()
            display.fill_circle(x, y + i * 22, r, dim_color_map[i])

# ---------------- Основной цикл ----------------

while True:
    x_val, y_val, z_val = gyro_accel.read_accel()

    if x_val > treshold:
        if time.ticks_diff(time.ticks_ms(), last_time) > 250:
            led_index = change_index(led_index, -1)
            last_time = time.ticks_ms()
            if last_index != led_index:
                beep(buzzer, freq_map[led_index])
                last_index = led_index

    elif x_val < -treshold:
        if time.ticks_diff(time.ticks_ms(), last_time) > 250:
            led_index = change_index(led_index, 1)
            last_time = time.ticks_ms()
            if last_index != led_index:
                beep(buzzer, freq_map[led_index])
                last_index = led_index

    update_leds(leds, led_index)
    time.sleep(0.1)