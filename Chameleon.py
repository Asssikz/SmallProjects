from pibody import ColorSensor, LEDTower

np = LEDTower(pin=16)
color_sensor = ColorSensor('H')

###--- Color Sensor Tester ---###
def colorsensor_mode(np, r, g, b):
    np.fill((r, g, b))
    np.write()
###--- Color Sensor Tester ---###

while True:
    r, g, b = color_sensor.readRGB()
    colorsensor_mode(np, r, g, b)
    print(r, g, b)


