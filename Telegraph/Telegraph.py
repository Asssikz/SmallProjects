from machine import Pin, PWM
from time import ticks_ms, ticks_diff, sleep

button_morse = Pin(4, Pin.IN)     
button_delete = Pin(6, Pin.IN)    

buzzer = PWM(Pin(0))              
led = Pin(2, Pin.OUT)             
morse_letter_dict = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z"
}

text = ""
morse_letter = ""
last_letter_time = ticks_ms()
last_display = ""

dash_threshold = 300        
long_press_space = 2000     
morse_pause = 1200          

def flash(duration_ms):
    buzzer.freq(600)
    buzzer.duty_u16(1000)
    led.value(1)
    sleep(duration_ms / 1000.0)
    buzzer.duty_u16(0)
    led.value(0)
    sleep(0.05)

def format_text_for_display(raw_text):
    if len(raw_text) > 16:
        return raw_text[-16:]
    return raw_text

def show(text_to_show):
    global last_display
    formatted = format_text_for_display(text_to_show)
    if formatted != last_display:
        print(formatted)
        last_display = formatted

def update_display():
    show(text)

print("Морзе запущен")
update_display()

while True:
    now = ticks_ms()

    if button_morse.value():
        press_start = ticks_ms()
        while button_morse.value():
            sleep(0.01)
        press_time = ticks_diff(ticks_ms(), press_start)

        if press_time > long_press_space:
            text += " "  
        elif press_time > dash_threshold:
            morse_letter += "-"
            flash(press_time)
        else:
            morse_letter += "."
            flash(press_time)

        last_letter_time = ticks_ms()
        update_display()

    if morse_letter and ticks_diff(ticks_ms(), last_letter_time) > morse_pause:
        letter = morse_letter_dict.get(morse_letter, "?")
        text += letter
        morse_letter = ""
        update_display()

    if button_delete.value():
        if text:
            text = text[:-1]
            update_display()
        sleep(0.3)  
