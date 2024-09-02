import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

import subprocess

def ping_ip(ip):
    """Ping a single IP address and return the result."""
    print(f"Pinging {ip}")  # Print the IP being pinged
    # Use subprocess to call the system ping command
    try:
        output = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    results = []
    # Use ThreadPoolExecutor to ping IPs concurrently
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            result = future.result()
            results.append(result)

    return results

def ip_to_int(ip):
    return sum([int(x) << (8 * (3 - i)) for i, x in enumerate(ip.split('.'))])

def int_to_ip(ip_int):
    return '.'.join([str((ip_int >> (8 * (3 - i))) & 0xFF) for i in range(4)])

def create_image(results, width):
    height = len(results) // width + (1 if len(results) % width > 0 else 0)
    image_data = np.zeros((height, width), dtype=np.uint8)

    for i, result in enumerate(results):
        image_data[i // width, i % width] = 255 if result == 1 else 0  # White for success, black for failure

    # If the last row is not completely filled, fill it with black pixels
    if len(results) % width != 0:
        image_data[-1, len(results) % width:] = 0

    image = Image.fromarray(image_data, 'L')  # 'L' mode for grayscale
    return image

def main():
    start_ip = input("Enter start IP (like 10.0.8.1) : ")  # Change to your starting IP
    end_ip = input("Enter end IP (like 10.0.8.255)")   # Change to your ending IP
    width = 16                   # Width of the image

    results = ping_ip_range(start_ip, end_ip)
    image = create_image(results, width)
    image.save("ping_results.png")

if __name__ == "__main__":
    main()
