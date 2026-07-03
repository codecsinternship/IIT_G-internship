import sys
import re
import serial
import serial.tools.list_ports

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)


class Voltmeter(QWidget):

    def __init__(self):
        super().__init__()

        self.serial_port = None

        self.setWindowTitle("Arduino Digital Voltmeter")
        self.setFixedSize(420, 260)

        # Title
        title = QLabel("DIGITAL VOLTMETER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        # Voltage Display
        self.voltageLabel = QLabel("0.00 V")
        self.voltageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltageLabel.setFont(QFont("Consolas", 36, QFont.Weight.Bold))
        self.voltageLabel.setStyleSheet("""
            QLabel{
                background:#111;
                color:#00FF66;
                border:2px solid gray;
                border-radius:8px;
                padding:15px;
            }
        """)

        # COM Port Selection
        self.portBox = QComboBox()
        self.load_ports()

        refreshBtn = QPushButton("Refresh Ports")
        refreshBtn.clicked.connect(self.load_ports)

        portLayout = QHBoxLayout()
        portLayout.addWidget(self.portBox)
        portLayout.addWidget(refreshBtn)

        # Connect Button
        self.connectBtn = QPushButton("Connect")
        self.connectBtn.clicked.connect(self.connect_serial)

        # Status
        self.status = QLabel("Disconnected")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.voltageLabel)
        layout.addLayout(portLayout)
        layout.addWidget(self.connectBtn)
        layout.addWidget(self.status)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)

    def load_ports(self):
        self.portBox.clear()

        ports = serial.tools.list_ports.comports()

        for port in ports:
            self.portBox.addItem(port.device)

    def connect_serial(self):

        if self.serial_port is None:
            port = self.portBox.currentText()
            if not port:
                QMessageBox.warning(self, "Warning", "No COM port selected!")
                return

            try:
                self.serial_port = serial.Serial(port, 9600, timeout=1)

                self.timer.start(100)

                self.status.setText("Connected")

                self.connectBtn.setText("Disconnect")

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

        else:

            self.timer.stop()

            self.serial_port.close()

            self.serial_port = None

            self.status.setText("Disconnected")

            self.connectBtn.setText("Connect")

    def read_serial(self):

        if self.serial_port.in_waiting:

            try:
                line = self.serial_port.readline().decode().strip()

                # Arduino Output:
                # Raw ADC: 421  |  Voltage: 2.06

                match = re.search(r"Voltage:\s*([\d.]+)", line)

                if match:
                    voltage = float(match.group(1))
                    self.voltageLabel.setText(f"{voltage:.2f} V")

            except:
                pass


app = QApplication(sys.argv)

window = Voltmeter()
window.show()

sys.exit(app.exec())
