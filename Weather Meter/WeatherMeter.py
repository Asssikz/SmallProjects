from pibody import ClimateSensor, Servo
from time import sleep

climate = ClimateSensor('A')

# Настройка сервопривода для измерения температуры
servo_temp = Servo(9)   # Подключен к пину 8

angle_temp = 90  # Начальное положение сервопривода
servo_temp.angle(angle_temp)  # Установка начального положения

sleep(1)

while True:
    temp = climate.read_temperature()  
    print(temp)
    
    angle_temp = 180 - (max(0, min(40, int(temp)))) * 180 / 40
    servo_temp.angle(angle_temp) 
    
    sleep(0.3)
