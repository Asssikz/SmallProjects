from pibody import Distance, Servo, Buzzer
from time import sleep

# --- Pins & Hardware ---
# Distance sensor in slot A
sensor = Distance("A")

# Servo on GP8 (PiBody dedicated servo header)
servo = Servo(8)

# Buzzer on GP6 (slot E left). Change if needed.
buzzer = Buzzer('E')

# --- Settings ---
TRIGGER_MM = 100     # 10 cm
OPEN_ANGLE = 90      # gate open angle
CLOSE_ANGLE = 0      # gate closed angle
OPEN_TIME_S = 5      # keep gate open for 5 seconds

# --- Helpers ---
def beep_open():
    """Single cheerful beep = opening."""
    buzzer.make_sound(1200, 1, 0.15)

def beep_close():
    """Double short beep = closing."""
    buzzer.make_sound(800, 1, 0.15)
    sleep(0.08)
    buzzer.make_sound(800, 1, 0.15)

# --- Main loop ---
while True:
    distance = sensor.read()   # distance in mm
    print("Distance:", distance, "mm")

    if distance == 20 or distance == 8190:
        continue

    if distance <= TRIGGER_MM:
        print("Object close! Opening gate...")
        beep_open()
        servo.angle(OPEN_ANGLE)
        sleep(OPEN_TIME_S)          # keep the gate open for N seconds

        print("Closing gate...")
        servo.angle(CLOSE_ANGLE)
        beep_close()
    else:
        # ensure servo is in default position when nothing is near
        servo.angle(CLOSE_ANGLE)

    sleep(0.1)  # small loop delay