"""
Serial Port Baud Rate Detector

This script lists available COM ports, prompts the user to select one,
and iterates over a list of baud rates, reading data from the selected
serial port. The loop can be exited by pressing Ctrl+C. Upon exiting,
the user can select the correct baud rate to open the port with miniterm.

Functions:
    set_com_port() -> str
    get_timeout_value(default: int) -> int
    read_from_serial(port: str, current_baud_rate: int, timeout: int) -> str
    set_baud_rate() -> int or None
    clear_screen() -> None
    baud_rate_detector(com_port: str) -> None
    miniterm(com_port: str, baud_rate: int) -> None
    main_menu(com_port: str = None, baud_rate: int = None) -> None
"""

from os import system, name
from typing import Optional
import time
import sys
import serial
import serial.tools
from serial.tools.list_ports import comports

baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]

def set_com_port() -> str:
    """
    Prompt the user to select a COM port.

    Returns:
        str: The device name of the selected COM port, or None if the user selects "None".
    """
    clear_screen()
    ports = list(comports())
    print("Available COM ports:")
    for i, port in enumerate(ports, 1):
        print(f"{i}: {port.device}")
    print(f"{len(ports) + 1}: None")

    try:
        port_index = int(input(f"Select a COM port (1-{len(ports) + 1}): ")) - 1
        if port_index == len(ports):
            return None
        else:
            return ports[port_index].device
    except ValueError:
        return None

def get_timeout_value(default: int = 5) -> int:
    """
    Prompt the user for a timeout value, allowing them to accept a default value.

    Args:
        default (int, optional): The default timeout value in seconds. Defaults to 5.

    Returns:
        int: The user-specified or default timeout value in seconds.
    """
    timeout_input = input(f"Enter timeout in seconds (default {default}s): ")
    return int(timeout_input) if timeout_input else default

def read_from_serial(port: str, current_baud_rate: int, timeout: int) -> str:
    """
    Read data from the specified serial port at the given baud rate for a given timeout period.

    Args:
        port (str): The device name of the COM port to read from.
        current_baud_rate (int): The baud rate at which to read the data.
        timeout (int): The duration in seconds for which to read the data.

    Returns:
        str: A string of readable characters received from the serial port.
    """
    received_data = []
    with serial.Serial(port, current_baud_rate, timeout=1) as serial_port:
        start_time = time.time()

        while time.time() - start_time < timeout:
            if serial_port.in_waiting > 0:
                byte_data = serial_port.read(1)
                byte_value = int.from_bytes(byte_data, byteorder='big')

                if 32 <= byte_value <= 126 or byte_value == 10 or byte_value == 13:
                    received_data.append(chr(byte_value))

    return ''.join(received_data)


def set_baud_rate() -> Optional[int]:
    """
    Prompt the user to select the correct baud rate after exiting the loop.

    Returns:
        int or None: The user-selected baud rate, or None if the user selects "None".
    """
    clear_screen()
    print("Select the correct baud rate or choose 'None' to exit:")
    for i, rate in enumerate(baud_rates, 1):
        print(f"{i}: {rate}")
    print(f"{len(baud_rates) + 1}: None")

    try:
        choice = int(input(f"Enter your choice (1-{len(baud_rates) + 1}): "))
        if choice == len(baud_rates) + 1:
            return None
        else:
            return baud_rates[choice - 1]
    except ValueError:
        return None

def clear_screen() -> None:
    """Clear the console screen."""
    system("cls" if name == "nt" else "clear")

def baud_rate_detector(com_port: str = None) -> None:
    """
    Detects the correct baud rate by iterating through common
    baud rates and reading from the serial port.

    Args:
        com_port (str): The device name of the COM port to read from.
    """
    clear_screen()

    if com_port is None:
        print("No COM port selected. Please select a COM port.")
        input("\nPress Enter to continue...")
        return

    timeout_seconds = get_timeout_value()

    # Inform the user how to exit the loop
    print("The loop will now start. Press Ctrl+C at any time to exit.")

    baud_rate_index = 0

    try:
        while True:
            current_baud_rate = baud_rates[baud_rate_index]
            print(f"Current baud rate: {current_baud_rate}")

            data = read_from_serial(com_port, current_baud_rate, timeout_seconds)
            if data:
                print(data)

            print("\n##################################################################\n")

            baud_rate_index = (baud_rate_index + 1) % len(baud_rates)

    except KeyboardInterrupt:
        return

def miniterm(com_port: str = None, baud_rate: int = None) -> None:
    """
    Runs miniterm with the specified port and baud rate.

    Args:
        com_port (str): The device name of the COM port.
        baud_rate (int): The baud rate to use with miniterm.
    """
    clear_screen()

    if com_port is None:
        print("No COM port selected. Please select a COM port.")
        input("\nPress Enter to continue...")
        return

    if baud_rate is None:
        print("No baud rate selected. Please run the baud rate detector.")
        input("\nPress Enter to continue...")
        return

    serial.tools.miniterm.main([com_port, str(baud_rate)])

def main_menu(com_port: str = None, baud_rate: int = None) -> None:
    """
    Main menu function to orchestrate the workflow: listing COM ports, selecting a port,
    setting a timeout, and reading from the serial port. The loop continues until
    the user interrupts with Ctrl+C. Upon exiting, the user is prompted to select
    the correct baud rate and optionally open the port with miniterm.

    Args:
        com_port (str, optional): The selected COM port. Defaults to None.
        baud_rate (int, optional): The selected baud rate. Defaults to None.
    """
    clear_screen()

    while True:
        print("Serial Port Tool")
        print("1. Baud rate detector")
        print("2. MiniTerm")
        print(f"3. Set COM Port [{com_port}]")
        print(f"4. Set Baud Rate [{baud_rate}]")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            baud_rate_detector(com_port)
        elif choice == "2":
            miniterm(com_port, baud_rate)
        elif choice == "3":
            com_port = set_com_port()
        elif choice == "4":
            baud_rate = set_baud_rate()
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")
        clear_screen()

def main():
    """
    Main function to run the script.
    
    This function initializes the main menu with no COM port or baud rate selected.
    """
    main_menu()


if __name__ == '__main__':
    main()
