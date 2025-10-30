from pibody import Buzzer, Button, GyroAxel
from time import sleep

sensor = GyroAxel('A')
btn = Button('F')
buzzer = Buzzer('D')
freq = 440 # Initial frequency
min_freq = 220
max_freq = 880

while True:
    gx, gy, gz = sensor.read_gyro()
    print(f'Gyro: x={gx}, y={gy}, z={gz}')
    sleep(0.1)

    # ax, ay, az = sensor.read_accel()
    # z = min(1.0, max(-1.0, round(ay-1, 1)))

    # freq = int(freq + (z * 10))
    # freq = min(max_freq, max(min_freq, freq))
    # print(f'Accel: z={z}, Freq={freq}')
    # buzzer.freq(freq)

    # if btn.value() == 1:
    #     buzzer.volume(0.2)
    # else:
    #     buzzer.volume(0.0)