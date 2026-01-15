from pibody import Distance, Servo, Buzzer
from time import sleep

# --- Модули ---
sensor = Distance("A")
servo = Servo(8)
buzzer = Buzzer("E")

# --- Функции сигналов ---
def beep_open():
    """Одно короткое 'весёлое' пи-пи при открытии."""
    buzzer.make_sound(1200, 1, 0.1)

def beep_close():
    """Два коротких 'пи' при закрытии."""
    buzzer.make_sound(800, 1, 0.1)
    sleep(0.1)
    buzzer.make_sound(800, 1, 0.1)

# --- Основной цикл ---
while True:
    distance = sensor.read()
    print("Distance:", distance, "mm")

    if distance in (20, 8190):
        continue

    if distance <= 100:
        print("Объект близко! Открываем ворота...")
        beep_open()
        servo.angle(90)
        sleep(5)

        print("Закрываем ворота...")
        servo.angle(0)
        beep_close()
    else:
        servo.angle(0)

    sleep(0.1) 