# Serial Port Baud Rate Detection and Miniterm Launcher

This Python script helps you detect the correct baud rate for a serial port by cycling through multiple baud rates and reading data from the specified COM port. Once the correct baud rate is identified, the script can automatically launch `miniterm` to monitor the serial port at the selected baud rate.

## Features

- **COM Port Selection**: Lists all available COM ports and allows you to select the one you want to work with.
- **Baud Rate Cycling**: Iterates through a list of common baud rates, reading data from the selected serial port.
- **User-Friendly Exit**: Press `Ctrl+C` at any time to exit the loop and select the correct baud rate.
- **Miniterm Integration**: After selecting the correct baud rate, the script can launch `miniterm` in a new process to monitor the serial port.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/serial-port-baudrate-detection.git
   cd serial-port-baudrate-detection
   ```

2. **Install Dependencies**
   Ensure you have Python installed. You will also need `pyserial` for serial communication:
   ```bash
   pip install pyserial
   ```

## Usage

1. **Run the Script**

   ```bash
   python serial_port_baudrate_detection.py
   ```

2. **Select COM Port**
   The script will list available COM ports. Select the one you want to monitor.

3. **Set Timeout**
   You can specify a timeout value (in seconds) for how long the script should try each baud rate. Press Enter to accept the default value.

4. **Cycle Through Baud Rates**
   The script will cycle through common baud rates, reading data from the selected COM port.

5. **Select Correct Baud Rate**
   After exiting the loop (using `Ctrl+C`), you can select the correct baud rate. If selected, the script will launch `miniterm` to monitor the port with that baud rate.

## Example

![Example GIF](link-to-example-gif-or-screenshot) _(Optional)_

## Known Issues

    Miniterm is not launching in testing within a virtualenv. Haven't had a chance to test

## Credits

This script was inspired by and adapted from the `baudrate` program by [devttys0](https://github.com/devttys0). The original `baudrate` program, which this script takes inspiration from, can be found [here](https://github.com/devttys0/baudrate).

Special thanks to c. heffner [devttys0](https://github.com/devttys0) for the original concept and implementation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or suggestions.

## Disclaimer

Use this script responsibly and ensure that you have permission to access and monitor the serial ports you are working with.
