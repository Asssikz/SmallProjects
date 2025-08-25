from pibody import (
    Display, ButtonLike, ColorSensor, DistanceSensor, ClimateSensor,
    Encoder, LED, Buzzer, Joystick, GyroAxelSensor
)
from time import sleep, ticks_ms
from machine import Pin

# ---------------------------
# Initialization
# ---------------------------

display = Display()

# Buttons
next_button = Pin(21, Pin.IN)
select_button = Pin(20, Pin.IN)

# Menu state
index = 0
state = "menu"
last_press = {"next": 0, "select": 0}

# Available module types
keys = ['LED', 'Buzzer', 'ButtonLike', 'Encoder', 'AnalogLike', 
    'ColorSensor', 'DistanceSensor', 'ClimateSensor', 'GyroAxelSensor']

MODULES = {
    "LED": (LED, ['A', 'B', 'C', 'D', 'E', 'F']),
    "Buzzer": (Buzzer, ['A', 'B', 'C', 'D', 'E', 'F']),
    "ButtonLike": (ButtonLike, ['A', 'B', 'C', 'D', 'E', 'F']),
    "Encoder": (Encoder, ['A', 'B', 'C', 'D', 'E', 'F']),
    "AnalogLike": (Joystick, ['C', 'F']),
    "ColorSensor": (ColorSensor, ['A']),
    "DistanceSensor": (DistanceSensor, ['A']),
    "ClimateSensor": (ClimateSensor, ['A']),
    "GyroAxelSensor": (GyroAxelSensor, ['A']),
}

# ---------------------------
# Utility functions
# ---------------------------

def debounce(button, key, delay=200):
    """Check button press with debounce."""
    if button.value() and ticks_ms() - last_press[key] > delay:
        last_press[key] = ticks_ms()
        return True
    return False


def update_display():
    """Update menu display."""
    uiux_display()
    for i, name in enumerate(keys):
        color = display.GREEN if i == index else display.WHITE
        display.text(f"{i+1}. {name}", 10, 10 + 16 * i, fg=color)

def uiux_display(cancel=False):
    if cancel:
        text_1 = "cancel"
        text_2 = "cancel"
    else:
        text_1 = "select"
        text_2 = "next"
    offset_1 = len(text_1) * 8 + 4
    offset_2 = len(text_2) * 8
    display.text(text_1, 10, 300)
    display.text("GP20", 10 + offset_1, 300, fg=display.CYAN)
    display.text(text_2, 230 - offset_2, 300)
    display.text("GP21", 230 - offset_2 - 4 - 8 * 4, 300, fg=display.CYAN)

def cancel_check():
    """Return to menu if button pressed."""
    global state
    if debounce(select_button, "select", 500) or debounce(next_button, "next", 500):
        state = "menu"
        display.fill(display.BLACK)
        update_display()
        return False
    return True


def create_slots(module_cls, slot_names):
    """Create and return module instances in given slots."""
    return [module_cls(slot) for slot in slot_names]


def reader(slots, names, func):
    """Display values from slots with custom reader."""
    for i, slot in enumerate(slots):
        val = func(slot)
        display.text(f"{names[i]}: {val}      ", 10, 90 + 16 * i)


# ---------------------------
# Module check functions
# ---------------------------

def check_led():
    slots = create_slots(LED, MODULES["LED"][1])
    while cancel_check():
        for i, slot in enumerate(slots):
            slot.on()
            display.text(f"{MODULES['LED'][1][i]} is ON", 10, 90 + 16 * i, fg=display.GREEN)
    for s in slots: s.off()


def check_buzzer():
    slots = create_slots(Buzzer, MODULES["Buzzer"][1])
    while cancel_check():
        for slot in slots:
            slot.beep(volume=0.05, duration=0.05)
            sleep(0.075)
    for s in slots: s.off()


def check_button():
    slots = create_slots(ButtonLike, MODULES["ButtonLike"][1])
    while cancel_check():
        reader(slots, MODULES["ButtonLike"][1], lambda x: "1" if x.value() else "0")


def check_encoder():
    slots = create_slots(Encoder, MODULES["Encoder"][1])
    for s in slots:
        s.set(min_val=0, max_val=10, incr=1, range_mode=s.RANGE_BOUNDED)
    while cancel_check():
        reader(slots, MODULES["Encoder"][1], lambda x: x.bar())


def check_analog():
    slots = create_slots(Joystick, MODULES["AnalogLike"][1])
    while cancel_check():
        reader(slots, MODULES["AnalogLike"][1], lambda x: x.read())
        sleep(0.05)


def check_color():
    slots = create_slots(ColorSensor, MODULES["ColorSensor"][1])
    while cancel_check():
        reader(slots, MODULES["ColorSensor"][1], lambda x: x.readRGB())
        sleep(0.05)


def check_distance():
    slots = create_slots(DistanceSensor, MODULES["DistanceSensor"][1])
    while cancel_check():
        reader(slots, MODULES["DistanceSensor"][1], lambda x: x.bar(width=15))


def check_climate():
    slots = create_slots(ClimateSensor, MODULES["ClimateSensor"][1])
    while cancel_check():
        reader(slots, MODULES["ClimateSensor"][1], lambda x: x.read_temperature())


def check_gyro():
    slots = create_slots(GyroAxelSensor, MODULES["GyroAxelSensor"][1])
    while cancel_check():
        reader(slots, MODULES["GyroAxelSensor"][1], lambda x: x.read_accel())


CHECK_FUNCTIONS = [
    check_led, check_buzzer, check_button, check_encoder,
    check_analog, check_color, check_distance, check_climate, check_gyro
]

# ---------------------------
# Main loop
# ---------------------------

update_display()

while True:
    if state == "menu":
        if debounce(next_button, "next"):
            index = (index + 1) % len(MODULES)
            update_display()
        if debounce(select_button, "select"):
            state = "checking"

    elif state == "checking":
        display.fill(display.BLACK)
        name = keys[index]
        display.text(name, 10, 16, font=display.font_bold, fg=display.CYAN)
        display.text("is checking", 10, 48, font=display.font_bold, fg=display.CYAN)
        uiux_display(cancel=True)

        CHECK_FUNCTIONS[index]()  # Run appropriate checker