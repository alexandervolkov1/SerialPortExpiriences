import random

import serial


def generate_signal(command):
    match command:
        case '#0A':
            return ''.join([
                f'{(i - 3) * 10.5 + random.random():+07.2f}' for i in range(8)
            ])
        case '#0B':
            return ''.join([
                f'{(i + 5) * 10.5 + random.random():+07.2f}' for i in range(8)
            ])


def start_server(port_name):
    ser = serial.Serial(port_name)
    while True:
        com = ser.readline().decode().strip()
        print(com)
        ser.write(f'{generate_signal(com)}\n'.encode())


if __name__ == '__main__':
    start_server('COM10')
