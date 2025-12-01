from pibody import Sound, LEDTower

led_tower = LEDTower("E")
mic = Sound('F')

max_deviation = 0 
decay_rate = 0.004

while True:
    value = mic.read_analog()

    deviation = abs(value - 0.5)
    if deviation > max_deviation:
        max_deviation = deviation
    else:
        max_deviation -= decay_rate
    
    max_deviation = max(max_deviation, 0)

    index = round(max_deviation / 0.5 * 8) - 1
    print(index)

    for i in range(8):
        if i <= index:
            led_tower[i] = (0, 50, 0)
        else:
            led_tower[i] = (0, 0, 0)
    led_tower.write()