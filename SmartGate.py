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
def move_servo(angle):
    """Move servo to given angle (0–180°). Adjust min/max if your servo differs."""
    min_u16 = 1638     # ~0.5 ms pulse @ 50 Hz -> 0°
    max_u16 = 8192     # ~2.5 ms pulse @ 50 Hz -> 180°
    duty = int(min_u16 + (angle / 180) * (max_u16 - min_u16))
    servo.duty_u16(duty)

def tone(freq, ms):
    """Play a tone on the buzzer at freq Hz for ms milliseconds."""
    buzzer.freq(freq)
    buzzer.duty_u16(32768)  # ~50% duty
    sleep(ms / 1000)
    buzzer.duty_u16(0)

def beep_open():
    """Single cheerful beep = opening."""
    tone(1200, 150)

def beep_close():
    """Double short beep = closing."""
    tone(800, 100)
    sleep(0.08)
    tone(800, 100)

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