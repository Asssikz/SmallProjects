from machine import Pin, PWM
from time import sleep
from pibody import ClimateSensor

climate = ClimateSensor('A')

# Настройка сервопривода для измерения температуры
servo_temp = PWM(Pin(9))   # Подключен к пину 8
servo_temp.freq(50)         # Частота для сервопривода

angle_temp = 90  # Начальное положение сервопривода
servo_temp.duty_u16(int(((angle_temp / 180) * 2 + 0.5) * 65535 / 20))  # Установка начального положения

# Настройка сервопривода для измерения влажности
servo_hum = PWM(Pin(8))   # Подключение к пину 9
servo_hum.freq(50)         # Частота для сервопривода

angle_hum = 180  # Начальное положение сервопривода для влажности
servo_hum.duty_u16(int(((angle_hum / 180) * 2 + 0.5) * 65535 / 20))  # Установка начального положения серво для влажности

sleep(1)

while True:
    try:
        # Считывание данных с датчика
        temp = climate.read_temperature()
        hum = climate.read_humidity()        
        
        angle_temp = 180 - (max(-10, min(40, int(temp[:-4]))) + 10) * 180 / 50 # Изменение угла на основе данных температуры
        servo_temp.duty_u16(int(((angle_temp / 180) * 2 + 0.5) * 65535 / 20)) # Установка положения для температуры через угол
        
        angle_hum = 180 - (int(hum[:-4]) * 180 / 100)  # Изменение угла на основе данных влажности
        servo_hum.duty_u16(int(((angle_hum / 180) * 2 + 0.5) * 65535 / 20))  # Установка положения для влажности через угол
        
    except Exception as e:
        print('Произошла ошибка:', e)

    sleep(0.3)
