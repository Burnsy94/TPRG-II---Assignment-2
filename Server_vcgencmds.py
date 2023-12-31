# TPRG II Assignment 2
# Alex Burns - 100885375

# Code taken from ChatGPT on November 27th, 2023. Prompted by asking "Complete this incomplete code. Add a total of 4 NEW vcgencmd calls and further process each. Add the detail to obtain each argument from the 4 new functions in the Server [the starter file is provided with the appropriate detail to get the core temperature, you need  to add 4 (four more arguments). Each argument should be sent to the client using a Json object"
import socket
import json
import os  # Code taken from ChatGPT on November 27th, 2023. Prompted by asking "My code is giving me errors and not recognizing the core temperature on vcgencmd module. Please incorporate the os module instead"

# Function to execute vcgencmd commands and return the result
def run_vcgencmd(command):
    return os.popen(f'vcgencmd {command}').read().strip()

# Function to get the core temperature of the Pi
def get_core_temperature():
    return run_vcgencmd('measure_temp')

# Function to get the core voltage of the Pi
def get_core_voltage():
    return run_vcgencmd('measure_volts core')

# Function to get the memory split between CPU and GPU
def get_memory_split():
    arm_memory = run_vcgencmd('get_mem arm')
    gpu_memory = run_vcgencmd('get_mem gpu')
    return {"ARM Memory": arm_memory, "GPU Memory": gpu_memory}

# Function to get the clock frequencies
def get_clock_frequencies():
    frequencies = {}
    for source in ['arm', 'core', 'H264', 'isp', 'v3d', 'uart', 'pwm', 'emmc', 'pixel', 'vec', 'hdmi', 'dpi']:
        freq = run_vcgencmd(f'measure_clock {source}')
        frequencies[source] = freq
    return frequencies

# Function to get the voltages of the SD card
def get_sdram_voltages():
    sdram_c = run_vcgencmd('measure_volts sdram_c')
    sdram_i = run_vcgencmd('measure_volts sdram_i')
    sdram_p = run_vcgencmd('measure_volts sdram_p')
    return {"SDRAM Controller Voltage": sdram_c, "SDRAM I/O Voltage": sdram_i, "SDRAM PHY Voltage": sdram_p}

# Function to get the throttled state of the system
def get_throttled():
    return run_vcgencmd('get_throttled')

# Function to get the codec status
def get_codec_status():
    codecs = ['H264', 'MPG2', 'WVC1', 'MPG4', 'MJPG', 'WMV9']
    codec_status = {}
    for codec in codecs:
        status = run_vcgencmd(f'codec_enabled {codec}')
        codec_status[codec] = status
    return codec_status

# Function to get the disk usage
def get_disk_usage():
    disk_usage = os.popen("df -h | grep /dev/root").read().strip()
    return {"Disk Usage": disk_usage}

# Server setup
s = socket.socket()
host = ''  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)

print(f"Server started. Listening on port {port}.")

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    data = {
        "Core Temperature": get_core_temperature(),
        "Core Voltage": get_core_voltage(),
        "Memory Split": get_memory_split(),
        "Clock Frequencies": get_clock_frequencies(),
        "SDRAM Voltages": get_sdram_voltages(),
        "Throttled State": get_throttled(),
        "Codec Status": get_codec_status(),
        "Disk Usage": get_disk_usage()
    }
    json_data = json.dumps(data, indent=4)  # Pretty print the data with an indent
    c.send(bytes(json_data, 'utf-8'))  # Send JSON string as bytes
    c.close()
    