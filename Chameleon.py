from pibody import ColorSensor, LEDTower

np = LEDTower()
color_sensor = ColorSensor('H')

while True:
    r, g, b = color_sensor.readRGB()
    np.fill((r, g, b))
    np.write()


