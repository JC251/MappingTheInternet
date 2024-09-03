import numpy as np
from PIL import Image
import subprocess
from math import ceil, sqrt
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_ip(ip):
    """Ping a single IP address and return the result."""
    print(f"Pinging {ip}")  # Print the IP being pinged
    # Use subprocess to call the system ping command
    try:
        output = subprocess.run(["ping", "-c", "1", "-W", "5", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 1 if output.returncode == 0 else 0  # Return 1 for success, 0 for failure
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return 0  # Return 0 for failure in case of an exception

def ping_ip_range(start_ip, end_ip):
    # Convert IP addresses to integers
    start = ip_to_int(start_ip)
    end = ip_to_int(end_ip)

    # Create a list to hold the IP addresses to ping
    ip_list = [int_to_ip(ip_int) for ip_int in range(start, end + 1)]

    results = [0] * len(ip_list)  # Preallocate results list
    # Use ThreadPoolExecutor to ping IPs concurrently
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_index = {executor.submit(ping_ip, ip): index for index, ip in enumerate(ip_list)}
        for future in as_completed(future_to_index):
            # Multithreading without having a race condition softwa
            index = future_to_index[future]  # Get the index of the completed future
            result = future.result()
            results[index] = result  # Write the result to the correct index

    return results

def ip_to_int(ip):
    return sum([int(x) << (8 * (3 - i)) for i, x in enumerate(ip.split('.'))])

def int_to_ip(ip_int):
    return '.'.join([str((ip_int >> (8 * (3 - i))) & 0xFF) for i in range(4)])

def create_image(results, width, img_format):

    if img_format == "S":
        height = ceil(sqrt(len(results)))
        width = ceil(sqrt(len(results)))
    else:
        height = len(results) // width + (1 if len(results) % width > 0 else 0)

    
    image_data = np.zeros((height, width), dtype=np.uint8)

    for i, result in enumerate(results):
        image_data[i // width, i % width] = 255 if result == 1 else 0  # White for success, black for failure

    # If the last row is not completely filled, fill it with black pixels
    if len(results) % width != 0:
        image_data[-1, len(results) % width:] = 0

    image = Image.fromarray(image_data, 'L')  # 'L' mode for grayscale
    return image
