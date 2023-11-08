# Apple Silicon M1 and M2 Temperature Sensor
## Purpose:
Create a solution to monitor the temperature sensors of Apple Silicon M1 and M2 chips, as the standard `powermetrics` utility is not available for Apple Silicon chips.

(Note: Command to get Apple Intel chip temperature: `sudo powermetrics --samplers smc |grep -i "CPU die temperature" `.)

## Code Summary:
    
### dependencies.sh:

1. Install `Homebrew`, `Python 3`, and `GCC` with the following:
    - `bash dependencies.sh`

### cpu_temp_and_stress_test.py:

- This python code continuously monitors the CPU temperature (specifically the cpu die temps), simulates device under heavy CPU load, and calculates sensor readings for temperature data.
    
### temp_sensor.m:
##### (from here: https://github.com/fermion-star/apple_sensors)

This Objective-C code's purpose is to retrieve and monitor sensor values, specifically power and thermal data, from Apple devices using HID services and events.

- Retrieves and monitors power and thermal data from Apple devices using HID services and events.

- Includes functions for interacting with HID services, obtaining product names, and retrieving sensor values.

## Usage:

1. Only need to execute the `cpu_temp_and_stress_test.py`, with the following:
    - `python3 cpu_temp_and_stress_test.py`
2. To stop, press `CTRL + C`.
- (Note: Script will automatically stop after 10 minutes)

## TO-DO:

1. Break down python code to be more modular.
2. Do more research on how to have compiled executables ready to use without having to install `GCC` when running tests on a Apple Silicon chips.
3. Error handling, logging, and automated testing.

## Resources Used:

- https://github.com/fermion-star/apple_sensors
- https://developer.apple.com/documentation/iokit
- https://docs.python.org/3/
- https://lifehacker.com/stress-test-your-mac-with-the-yes-command-1564681908
- https://github.com/acidanthera/VirtualSMC/blob/master/Docs/SMCSensorKeys.txt
