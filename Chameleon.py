from pibody import ColorSensor, LEDTower

np = LEDTower(pin=16)
color_sensor = ColorSensor('H')

###--- Color Sensor Tester ---###
def colorsensor_mode(np, r, g, b, leds_num=8):
    for i in range(leds_num):
        np[i] = (r, g, b)
    np.write()
###--- Color Sensor Tester ---###

while True:
    try:
        r, g, b = color_sensor.readRGB()
        colorsensor_mode(np, r, g, b)
        print(r, g, b)
    except Exception as e:
        print(f"Error starting tester: {e}")

