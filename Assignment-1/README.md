# Arduino Voltmeter GUI

A desktop app that reads live voltage readings from an Arduino over USB serial and displays them on an analog gauge with a numeric readout. Built with **PySide6** (Qt for Python) and serial I/O via **QtSerialPort**.

## Features
- Real-time analog gauge with needle deflection
- Live numeric voltage readout
- Serial port scanning and manual connect/disconnect
- Configurable for 5V (Arduino Uno/Nano) or 3.3V (ESP32) boards

## Project Structure
```
voltmeter/
├── main.py            # GUI application (entry point)
└── requirements.txt   # Python dependencies
```

## Prerequisites
- Python 3.10+
- An Arduino (or ESP32) flashed with a compatible sketch (see below)
- USB driver for your board (e.g. CH340/FTDI) if ports don't show up

## Setup

```bash
# 1. Create and activate a virtual environment
cd voltmeter
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

Confirm your prompt shows `(venv)` before proceeding. If installation fails, run `pip install --upgrade pip` and retry.

## Arduino Sketch

The board must print **one plain number per line** at **9600 baud** (must match `BAUD_RATE` in `main.py`):

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  int rawValue = analogRead(A0);
  float voltage = rawValue * (5.0 / 1023.0);
  Serial.println(voltage);
  delay(200);
}
```

> **Using a 3.3V board (e.g. ESP32)?** Update both:
> - Arduino: `voltage = rawValue * (3.3 / 4095.0);` (12-bit ADC)
> - `main.py`: `GAUGE_MAX_VOLTS = 3.3`

After uploading, verify correct values in the Arduino IDE Serial Monitor, then **close the Serial Monitor** — only one program can hold the COM port at a time.

## Running the App

```bash
python main.py
```

1. Click **Refresh Ports** if your Arduino isn't listed.
2. Select the Arduino's port (check Device Manager on Windows, or `ls /dev/tty*` on macOS/Linux).
3. Click **Connect** — status should read `Connected to <port>`.
4. Vary the analog input (e.g. a potentiometer on A0) and confirm the needle and readout update live.
5. Click **Disconnect** to release the port cleanly.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: PySide6` | venv not activated, or dependencies not installed |
| No ports in dropdown | Arduino unplugged, or missing USB driver |
| "Could not open port" / access denied | Close the Arduino IDE Serial Monitor |
| Needle stuck at 0 | Baud rate mismatch, or board isn't printing per-line values — check in Serial Monitor |
| Garbage/NaN readings | Wrong analog reference voltage for your board (5V vs 3.3V) |
| Blank/frozen window | Run `python main.py` using the venv's Python, not system Python |

## Success Criteria
App connects to the Arduino's serial port and the gauge needle deflects in real time in response to analog input, with the voltage readout updating live.
