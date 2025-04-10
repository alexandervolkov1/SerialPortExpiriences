import time

import serial


commands = ['#0A', '#0B']
ser = serial.Serial('COM11')

while True:
    for command in commands:
        ser.write(f'{command}\n'.encode())
        answer = ser.readline().decode().strip()
        print(answer)
    time.sleep(3)
