import subprocess
import time
import os
import re
import platform
import multiprocessing


def dependencies_check():
    try:
        # Try to get the developer directory path
        subprocess.check_output(['xcode-select', '--print-path'])
        print("Command line developer tools are already installed.")
    except subprocess.CalledProcessError:
        print("Command line developer tools are not installed. Installing...")
        subprocess.run(['xcode-select', '--install'])
        print("\nCommand line developer tools have been installed.\n")


def stress_test(duration):
    num_cores = multiprocessing.cpu_count()
    # Run 'yes > /dev/null &' on all but one core
    for _ in range(num_cores - 1):
        subprocess.Popen("yes > /dev/null &", shell=True)


# determine the processor type of the mac and run code for the given type
def run_use_case(timeout_duration):
    processor_type = platform.processor()
    if processor_type.startswith("arm"):
        if not os.path.isfile('./sensors'):
            compile_command = ["gcc", "-framework", "Foundation", "-framework", "IOKit", "temp_sensor.m", "-o", "sensors"]
            subprocess.run(compile_command)

        run_command = ["./sensors"]

        with open('data.txt', 'w') as f:
            proc = subprocess.Popen(run_command, stdout=f)
            # Let it run for x seconds
            try:
                proc.wait(timeout=timeout_duration)
            except subprocess.TimeoutExpired:
                proc.kill()
    elif 'intel' in processor_type.lower():
        # Run terminal command to get CPU temperature for Intel Mac
        terminal_command = ["sudo", "powermetrics", "--samplers", "smc"]
        grep_command = ["grep", "-i", "CPU die temperature"]
        process = subprocess.Popen(terminal_command, stdout=subprocess.PIPE)
        output = subprocess.check_output(grep_command, stdin=process.stdout)
        process.wait()
        print(output.decode())
    else:
        print('Invalid processor type')



# read dirty data and output as a dictionary like: {'sensor_name': 10.00, ...}
def parse_output():
    # Read the output file
    with open('data.txt', 'r') as f:
        data = f.read()

    # Split the data by comma and new line to get individual sensor readings
    readings = data.split("\n")

    # Initialize empty lists for sensor names and values
    sensor_names = []
    sensor_values = []

    for reading in readings:
        # Split each reading by comma
        elements = reading.split(", ")
        # If the length of the elements is more than 1, it is a reading
        # The first line containing the sensor names have more than 1 element
        # The rest of the lines contain the sensor values
        if len(elements) > 1:
            # If the elements contain characters, it is a sensor name
            # Else, it is a sensor value
            if any(char.isalpha() for char in elements[0]):
                sensor_names = elements
            else:
                sensor_values.append(list(map(float, elements[:-1])))
    # print(sensor_names)
    # print(sensor_values)
    # Map the sensor names to their respective values
    sensor_data = []
    for values in sensor_values:
        sensor_map = dict(zip(sensor_names, values))
        sensor_data.append(sensor_map)

    return sensor_data


# extract the die temp sensors names along with the value associated with it into a new dictionary
def extract_tdie_data(sensor_data):
    filtered_data = []

    # Compile the regex pattern for matching
    pattern = re.compile("PMU tdie\d+$")

    # Iterate over the sensor_data
    for data_dict in sensor_data:
        # Dictionary comprehension to filter for keys that match "PMU tdieX"
        filtered_dict = {key: value for key, value in data_dict.items() if pattern.match(key)}
        filtered_data.append(filtered_dict)

    return filtered_data


# calculate the average of all of the sensors for the given processor then find the avergae of them to output
def calculate_averages(filtered_data):
    # Initialize list to store the average sensor readings
    average_data_list = []

    # Iterate over the dictionaries in filtered_data
    for i, data_dict in enumerate(filtered_data):
        # Compute the sum of sensor values
        total = sum(data_dict.values())
        # Compute the average of sensor values
        average = total / len(data_dict)
        # Add the computed average to a new dictionary
        average_data = {}
        average_data['CPU Die Temperature'] = average
        # Append the new dictionary to the list
        average_data_list.append(average_data)

    return average_data_list


dependencies_check()
start_time = time.time()
stress_test_started = False
try:
    print("Normal CPU Temperature...\n")
    while True:
        # Run the Objective-C code
        run_use_case(.5)  # timeout duration

        # Parse the output
        sensor_data = parse_output()

        # Extract PMU tdie lines with associated numbers
        filtered_data = extract_tdie_data(sensor_data)

        # Call the calculate_averages function
        average_data_list = calculate_averages(filtered_data)

        # Print readings to the terminal
        for average_data in average_data_list:
            for key, value in average_data.items():
                print(f"{key}: {round(value, 2)} C\n")

        # After 10 seconds, start the stress test if it hasn't started yet
        if time.time() - start_time > 10 and not stress_test_started:
            print("Starting Stress Test...")
            print("(To stop, press Ctrl + C)")
            print("(Will automatically stop after 10 minutes)\n")
            stress_test(10)
            stress_test_started = True

        # After 10 minutes, stop the stress test
        if time.time() - start_time > 610:
            print("Stopped Stress Test!")
            subprocess.run("killall yes", shell=True)
            break

        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated. Goodbye, World!")
    # Terminate the 'yes' processes
    subprocess.run("killall yes", shell=True)
    os._exit(0)
