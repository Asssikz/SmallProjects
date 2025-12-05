from pibody import Display, LED
from time import ticks_ms, ticks_diff, ticks_add, sleep_ms
import math

# ----------------------
# Константы "геометрии"
# ----------------------
CENTER_X = 120
CENTER_Y = 120

CLOCK_RADIUS = 90
HOUR_HAND_RADIUS = 50
MIN_HAND_RADIUS = 60
SEC_HAND_RADIUS = 68
TICK_RADIUS = 79

# Позиции текста
LOGO_X = 80
LOGO_Y = 216

TEXT_X = 10
TEXT_SEC_Y = 250
TEXT_MIN_Y = 266
TEXT_HOUR_Y = 282

DEG2RAD = math.pi / 180
TICK_INTERVAL_MS = 1000  # 1 секунда

# ----------------------
# Инициализация
# ----------------------
d = Display()
buzzer = LED("A")  # LED, используемый как "тик" для баззера

# Стартовое "виртуальное" время в секундах
seconds = 10500


# ----------------------
# Вспомогательные функции
# ----------------------
def angle_to_xy(angle_deg, radius):
    """Перевод угла (в градусах) и радиуса в координаты x, y."""
    rad = angle_deg * DEG2RAD - math.pi / 2
    x = round(CENTER_X + radius * math.cos(rad))
    y = round(CENTER_Y + radius * math.sin(rad))
    return x, y


def compute_angles(total_seconds):
    """Считаем углы для часовой, минутной и секундной стрелок."""
    sec = total_seconds % 60
    minutes_total = total_seconds / 60
    min_ = minutes_total % 60
    hours_total = minutes_total / 60
    hour = hours_total % 12

    s_angle = sec * 6          # 360 / 60
    m_angle = min_ * 6         # 360 / 60
    h_angle = hour * 30        # 360 / 12

    return h_angle, m_angle, s_angle


def draw_clock_face():
    """Статичный фон: круг, деления/цифры, логотип."""
    # Циферблат
    d.circle(CENTER_X, CENTER_Y, CLOCK_RADIUS, d.WHITE)

    # Цифры 1..12
    for i in range(12):
        angle_deg = i * 30
        x, y = angle_to_xy(angle_deg + 30, TICK_RADIUS)
        d.text(str(i + 1), x - 4, y - 6)

    # Логотип
    d.text("CLOCK", LOGO_X, LOGO_Y, font=d.font_bold)


def draw_hand(angle_deg, radius, color):
    """Нарисовать одну стрелку от центра к заданному углу."""
    x, y = angle_to_xy(angle_deg, radius)
    d.line(x, y, CENTER_X, CENTER_Y, color)


def erase_hand(angle_deg, radius):
    """Стереть стрелку, нарисовав поверх неё чёрную линию."""
    draw_hand(angle_deg, radius, d.BLACK)


def draw_all_hands(h_angle, m_angle, s_angle):
    """Нарисовать все три стрелки."""
    draw_hand(h_angle, HOUR_HAND_RADIUS, d.GREEN)
    draw_hand(m_angle, MIN_HAND_RADIUS, d.RED)
    draw_hand(s_angle, SEC_HAND_RADIUS, d.WHITE)


def erase_all_hands(h_angle, m_angle, s_angle):
    """Стереть все три стрелки по их прежним углам."""
    erase_hand(h_angle, HOUR_HAND_RADIUS)
    erase_hand(m_angle, MIN_HAND_RADIUS)
    erase_hand(s_angle, SEC_HAND_RADIUS)


def draw_time_text(total_seconds):
    """Обновить текст с текущими часами/минутами/секундами."""
    sec = total_seconds % 60
    minutes_total = total_seconds / 60
    min_ = int(minutes_total % 60)
    hours_total = minutes_total / 60
    hour = int(hours_total % 12)

    # пробелы в конце строки нужны, чтобы затирать старые цифры
    d.text(f"hours:   {hour:2d}  ", TEXT_X, TEXT_SEC_Y)
    d.text(f"minutes: {min_:2d}  ", TEXT_X, TEXT_MIN_Y)
    d.text(f"seconds: {sec:2d}  ", TEXT_X, TEXT_HOUR_Y)


# ----------------------
# Стартовая отрисовка
# ----------------------
draw_clock_face()

h_angle, m_angle, s_angle = compute_angles(seconds)
h_prev, m_prev, s_prev = h_angle, m_angle, s_angle

draw_all_hands(h_angle, m_angle, s_angle)
draw_time_text(seconds)

# Запускаем точный таймер
last_tick = ticks_ms()

# ----------------------
# Основной цикл
# ----------------------
while True:
    now = ticks_ms()

    # Если прошла секунда — обновляем состояние
    if ticks_diff(now, last_tick) >= TICK_INTERVAL_MS:
        last_tick = ticks_add(last_tick, TICK_INTERVAL_MS)

        # Стираем старые стрелки
        erase_all_hands(h_prev, m_prev, s_prev)

        # Обновляем время
        seconds += 1
        h_angle, m_angle, s_angle = compute_angles(seconds)

        # Рисуем новые стрелки и текст
        draw_all_hands(h_angle, m_angle, s_angle)
        draw_time_text(seconds)

        # "Тик"
        buzzer.toggle()

        # Запоминаем текущие углы как "предыдущие"
        h_prev, m_prev, s_prev = h_angle, m_angle, s_angle

    # Чтоб не жечь CPU вхолостую
    sleep_ms(5)
