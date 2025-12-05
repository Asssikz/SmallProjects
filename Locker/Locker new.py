from pibody import Encoder, LEDTower, Button, Buzzer, Servo
from time import sleep, ticks_ms

# ---------- Hardware ----------
encoder = Encoder('B')      # крутилка: выбираем цифру
button  = Button('A')       # кнопка: подтверждаем текущую цифру
buzzer  = Buzzer('E')
servo   = Servo(8)
np      = LEDTower('H')

encoder.wrap(0, 7)          # цифры 0..7 из энкодера

# ---------- Config ----------
PASSWORD       = [3, 1, 4]
TIMEOUT_MS     = 15000
START_ANGLE    = 90
TARGET_ANGLE   = 125

# NeoPixel цвета
BRIGHTNESS     = 1.0
SELECTED_COLOR = (0, 0, 255)   # выбранная текущая цифра
INPUT_COLOR    = (255, 255, 0) # уже введённые позиции
OK_COLOR       = (0, 255, 0)
ERR_COLOR      = (255, 0, 0)
SLEEP_COLOR    = (20, 40, 120)
BLACK          = (0, 0, 0)
SLEEP_ANIM     = "BAR"         # "BAR" или "RING"

# ---------- State ----------
input_buf = []            # текущий ввод (список чисел)
last_action = ticks_ms()
asleep = False
prev_btn = 0              # для детекта фронта нажатия

# ---------- Helpers ----------
def np_set(i, color, brightness=BRIGHTNESS):
    np[i] = tuple(int(c * brightness) for c in color)

def np_clear():
    for i in range(len(np)):
        np[i] = BLACK
    np.write()

def np_show_input(current_val):
    """Подсветка: текущая ячейка — синий, введённые позиции — жёлтые."""
    for i in range(len(np)):
        if i in input_buf:
            np_set(i, INPUT_COLOR)
        elif i == current_val:
            np_set(i, SELECTED_COLOR)
        else:
            np_set(i, BLACK)
    np.write()

def np_blink_all(color, times=6, dt=0.1):
    for k in range(times):
        for i in range(len(np)):
            np_set(i, color if k % 2 == 0 else BLACK)
        np.write()
        sleep(dt)

def buzz_ok():    buzzer.make_sound(2000, 1, 0.1)
def buzz_err():   buzzer.make_sound( 200, 1, 0.5)
def buzz_click(): buzzer.make_sound(  64, 1, 0.02)

def sleep_anim_ring():
    for shift in range(len(np)):
        for j in range(len(np)):
            idx = (j + shift) % len(np)
            br = ((j + 1) / len(np)) ** 2
            np_set(idx, SLEEP_COLOR, br)
        if not asleep: return False
        np.write(); sleep(0.07)
    return True

def sleep_anim_bar():
    n = len(np)
    for t in range(n * 2 - 1):
        idx = abs(n - t - 1)
        for j in range(n):
            dist = abs(j - idx) / n
            br = (1 - dist) ** 3
            np_set(j, SLEEP_COLOR, br)
        if not asleep: return False
        np.write(); sleep(0.07)
    return True

def go_sleep():
    global asleep
    asleep = True
    anim = sleep_anim_bar if SLEEP_ANIM == "BAR" else sleep_anim_ring
    while anim():
        pass

def wake():
    global asleep, last_action
    asleep = False
    np_clear()
    buzz_click()
    last_action = ticks_ms()

def submit_and_feedback(is_ok):
    if is_ok:
        buzz_ok()
        np_blink_all(OK_COLOR)
        servo.on()
        servo.angle(TARGET_ANGLE)
        sleep(0.1)
        servo.off()
        sleep(3)
        servo.on()
        servo.angle(START_ANGLE)
        sleep(0.1)
        servo.off()
    else:
        np_blink_all(ERR_COLOR)
        buzz_err()
        sleep(0.5)
    np_clear()

# ---------- Init ----------
servo.angle(START_ANGLE)
np_clear()

# ---------- Main loop ----------
while True:
    servo.off()
    # 1) Чтение энкодера — только для выбора текущего числа
    val = encoder.value()          # 0..7
    np_show_input(val)
    last_action = ticks_ms()       # любое вращение — активность

    # 2) Фронт нажатия кнопки = добавить текущее число
    cur_btn = button.value()
    if cur_btn and not prev_btn:   # нажали сейчас
        input_buf.append(val)
        buzz_click()
        np_show_input(val)         # обновим подсветку «введённая позиция»
        last_action = ticks_ms()

        # Если собрали длину пароля — проверяем сразу
        if len(input_buf) == len(PASSWORD):
            ok = (input_buf == PASSWORD)
            submit_and_feedback(ok)
            input_buf.clear()
            encoder.reset()        # вернём «курсор» к 0
            servo.on()
            servo.angle(START_ANGLE)
            sleep(0.1)

    prev_btn = cur_btn

    # 3) Тайм-аут простоя — усыпляем анимацией
    if (ticks_ms() - last_action) > TIMEOUT_MS and not asleep:
        np_clear()
        encoder.reset()
        servo.on()
        servo.angle(START_ANGLE)
        sleep(0.1)
        go_sleep()

    # 4) Любое действие будит систему
    if asleep and (cur_btn or encoder.direction() != 0):
        wake()

    sleep(0.01)  # лёгкий троттлинг цикла