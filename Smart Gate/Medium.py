from pibody import Distance, Servo
from time import sleep

# --- Модули ---
sensor = Distance("A")
servo = Servo(8)

# --- Настройки ---
TRIGGER_MM = 100     # Порог срабатывания — 10 см
OPEN_ANGLE = 90
CLOSE_ANGLE = 0

while True:
    distance = sensor.read()
    print("Distance:", distance, "mm")

    # Игнорируем некорректные значения
    if distance in (20, 8190):
        continue

    if distance <= TRIGGER_MM:
        print("Объект близко! Открываем ворота...")
        servo.angle(OPEN_ANGLE)
    else:
        print("Объект далеко. Закрываем ворота...")
        servo.angle(CLOSE_ANGLE)

    sleep(0.1) 