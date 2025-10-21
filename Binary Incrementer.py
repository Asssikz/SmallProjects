from pibody import Encoder, LEDTower

encoder = Encoder('C')
encoder.wrap(0, 255)
led = LEDTower(8)
binary = [0] * 8

while True:
    value = encoder.value()
    for i in range(8):
        binary[i] = (value // (2 ** (7 - i))) % 2
    for i in range(8):
        if binary[i] == 1:
            led[i] = (50, 50, 50)
        else:
            led[i] = (0, 0, 0)
    led.write()