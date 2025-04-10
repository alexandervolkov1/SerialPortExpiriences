import random
import sys

import serial
from PyQt6 import QtWidgets
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QIODevice


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


class SerialPortManager(QObject):
    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.port = QSerialPort()
        self.port.readyRead.connect(self.on_ready_read)

    def open_port(self, port_name):
        if self.port.isOpen():
            self.port.close()
        self.port.setPortName(port_name)
        self.port.open(QIODevice.ReadWrite)

    @pyqtSlot()
    def on_ready_read(self):
        pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Harmonic Signal Generator')

        self.start_stop_button = QtWidgets.QPushButton(text='START')
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.clicked.connect(self.start_stop_action)

        available_ports = [port.portName() for port in QSerialPortInfo().availablePorts()]
        self.comport_box = QtWidgets.QComboBox()
        self.comport_box.addItems(available_ports)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.comport_box)
        self.layout.addWidget(self.start_stop_button)

        root_widget = QtWidgets.QWidget()
        root_widget.setLayout(self.layout)

        self.setCentralWidget(root_widget)

    def start_stop_action(self):
        match self.start_stop_button.isChecked():
            case True:
                self.start_stop_button.setText('STOP')
                self.comport_box.setEnabled(False)
                self.start_server(self.comport_box.currentText())
            case False:
                self.start_stop_button.setText('START')
                self.comport_box.setEnabled(True)
                self.stop_server(self.comport_box.currentText())

    def start_server(self, port_name):
        ser = serial.Serial(port_name)
        while True:
            com = ser.readline().decode().strip()
            print(com)
            ser.write(f'{generate_signal(com)}\n'.encode())

    def stop_server(self, port_name):
        pass





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
