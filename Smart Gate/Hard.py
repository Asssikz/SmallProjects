from pibody import Distance, Servo, Buzzer
from time import sleep

# --- Модули ---
sensor = Distance("A")
servo = Servo(8)
buzzer = Buzzer("E")

# --- Настройки ---
TRIGGER_MM = 100     # 10 см
OPEN_ANGLE = 90
CLOSE_ANGLE = 0
OPEN_TIME_S = 5

# --- Функции сигналов ---
def beep_open():
    """Одно короткое 'весёлое' пи-пи при открытии."""
    buzzer.make_sound(1200, 1, 0.15)

def beep_close():
    """Два коротких 'пи' при закрытии."""
    buzzer.make_sound(800, 1, 0.15)
    sleep(0.08)
    buzzer.make_sound(800, 1, 0.15)

# --- Основной цикл ---
while True:
    distance = sensor.read()
    print("Distance:", distance, "mm")

    if distance in (20, 8190):
        continue

    if distance <= TRIGGER_MM:
        print("Объект близко! Открываем ворота...")
        beep_open()
        servo.angle(OPEN_ANGLE)
        sleep(OPEN_TIME_S)

        print("Закрываем ворота...")
        servo.angle(CLOSE_ANGLE)
        beep_close()
    else:
        servo.angle(CLOSE_ANGLE)

    sleep(0.1) 