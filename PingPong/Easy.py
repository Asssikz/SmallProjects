from pibody import GyroAccel, LED
import time

treshold = 0.5
led_index = 0
last_time = 0

led1 = LED("A")
led2 = LED("B")
led3 = LED("C")
leds = [led1, led2, led3]

sensor = GyroAccel("E")

def change_index(index, change):
    index += change
    index = min(max(index, 0), len(leds) - 1)
    return index

def update_leds(leds, index):
    for i in range(len(leds)):
        if i == index:
            leds[i].on()
        else:
            leds[i].off()

def check_time(last_time):
    if time.ticks_diff(time.ticks_ms(), last_time) > 250:
        return True
    return False

while True:
    ax, ay, az = sensor.read_accel()

    if ax > treshold:
        if check_time(last_time):
            led_index = change_index(led_index, -1)
            last_time = time.ticks_ms()

    elif ax < -treshold:
        if check_time(last_time):
            led_index = change_index(led_index, 1)  
            last_time = time.ticks_ms()

    update_leds(leds, led_index)
    time.sleep(0.1)