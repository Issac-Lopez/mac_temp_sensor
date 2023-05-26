# Purpose:
The purpose of this project is to create a way to view the temperature of the M1 and M2 chip sensors. The `powermetrics` utility is not available on M1 and M2 chips because it relies on Intel-specific hardware features and interfaces that are not present in Apple Silicon-based processors.

# Code Summary
    
## dependencies.sh:

1. Install `Homebrew`, `Python 3`, and `GCC` with the following:
    - `bash dependencies.sh`

## cpu_temp_and_stress_test.py:

This code continuously monitors the CPU temperature, performs stress testing, and calculates average sensor readings for temperature data.

1. Imports necessary modules: subprocess, time, os, re, platform, and multiprocessing.

2. Defines functions for stress testing the CPU, running use cases based on the processor type, parsing output data, extracting specific sensor data, and calculating sensor data averages.

3. Initializes variables and starts a loop for temperature monitoring and stress testing.

4. Within the loop, it runs use cases to obtain CPU temperature readings, parses the output, filters and extracts specific sensor data, calculates average values, and prints the average sensor readings.

5. It starts a stress test after a certain time and stops the stress test after a specified duration.

    
## temp_sensor.m:
##### (from here: https://github.com/fermion-star/apple_sensors)

This code's purpose is to retrieve and monitor sensor values, specifically power and thermal data, from Apple devices using HID services and events.

1. It includes necessary frameworks and declares functions and types from the IOKit framework for interacting with HID (Human Interface Device) services and events.

2. It defines a function, matching, that creates a dictionary representing matching criteria for sensors based on given usage page and usage values.

3. It defines functions, getProductNames, getPowerValues, and getThermalValues, which retrieve product names and sensor values from HID services based on the provided matching criteria.

4. It includes functions, dumpValues and dumpNames, for printing values and names to the console.

5. It provides helper functions, currentArray, voltageArray, and thermalArray, which create matching criteria and retrieve arrays of product names for current, voltage, and thermal sensors, respectively.

6. It includes functions, returnCurrentValues, returnVoltageValues, and returnThermalValues, which create matching criteria and retrieve arrays of sensor values for current, voltage, and thermal sensors, respectively.

7. The main function demonstrates the usage of the above functions by creating matching criteria, obtaining product names and sensor values, and continuously printing the values to the console.

# How to run:

1. Only need to execute the `cpu_temp_and_stress_test.py`, with the following:
    - `python3 cpu_temp_and_stress_test.py`
2. To stop, press `CTRL + D`.

# TO-DO:

1. Break down python code to be more modular.
2. Do more research on how to have compiled executables ready to use without having to install `GCC` when running tests on a Mac Book/iMac/Mac Mini.
3. Error handling, logging, and automated testing.
4. Add demo video.

# Resources Used:

- https://github.com/Issac-Lopez/apple_sensors/blob/master/temp_sensor.m
- https://github.com/fermion-star/apple_sensors
- https://developer.apple.com/documentation/iokit
- https://stackoverflow.com/
- https://docs.python.org/3/
- https://lifehacker.com/stress-test-your-mac-with-the-yes-command-1564681908
- https://github.com/acidanthera/VirtualSMC/blob/master/Docs/SMCSensorKeys.txt
