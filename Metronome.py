from pibody import LED
from time import ticks_ms, ticks_diff

led1 = LED('A')
led2 = LED('B')
buzzer = LED('D')

led1.on()
led2.off()

last_time = 0
bpm = 110   

def check_time(last_time):
    if ticks_diff(ticks_ms(), last_time) > bpm_in_ms:
        return True
    return False

bpm_in_ms = 60 / bpm * 1000
print(bpm_in_ms)

while True:
    if check_time(last_time):
        last_time = ticks_ms()
        led1.toggle()
        led2.toggle()
        buzzer.toggle()