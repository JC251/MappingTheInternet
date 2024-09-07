#!/usr/bin/env python
from def_func import ping_ip_range, create_image, scale_image  # Import the functions from def_func.py
import os
import time
import threading

def get_save_location():
    filename = input("Enter the filename (without extension): ")  # Ask for the filename
    directory = input("Enter the directory to save the file (leave blank for current directory): ")  # Ask for the directory

    if not directory:  # If no directory is provided, use the current directory
        directory = os.getcwd()

    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist. Using current directory instead.")
        directory = os.getcwd()

    return os.path.join(directory, f"{filename}.png")  # Return the full path for the file

def timer_thread(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        if elapsed_time >= 7:
            print(f"{int(elapsed_time)} seconds have passed.")
            time.sleep(10)  # Wait for another 10 seconds
        else:
            time.sleep(1)  # Check every second

def main():
    start_ip = input("Enter start IP (like 10.0.8.1): ")  # Change to your starting IP
    end_ip = input("Enter end IP (like 10.0.8.255): ")   # Change to your ending IP


    while True:
        user_input = input("Enter 'S' for single format or a number for width: ")


        if user_input.upper() == 'S':
            img_format = 'S'
            width = None  # No width needed for single format
            print(f"Image format set to: {img_format}")
            break  # Exit the loop

        elif user_input.isdigit():  # Check if the input is a number
            img_format = 'D'
            width = int(user_input)  # Convert input to an integer
            print(f"Image format set to: {img_format}, Width set to: {width}")
            break  # Exit the loop

        else:
            print("Invalid input. Please try again.")
        
    
    while True:
        scale_input = input("Enter scale factor of output image (positive integer): ")

        if scale_input.isdigit() and int(scale_input) > 0:  # Check if the scale input is a positive integer
            scale = int(scale_input)
            break
        else:
            print("Invalid input. Please try again.")

        

    # Start the timer thread
    start_time = time.time()
    stop_event = threading.Event()  # Create a stop event
    timer = threading.Thread(target=timer_thread, args=(start_time, stop_event))
    timer.daemon = True  # This allows the thread to exit when the main program exits
    timer.start()

    # Start the execution of the main tasks
    results = ping_ip_range(start_ip, end_ip)
    image = create_image(results, width, img_format)
    scaled_image = scale_image(image, scale)

    # Stop the timer before saving the image
    stop_event.set()  # Signal the timer thread to stop

    total_time = time.time() - start_time
    save_path = get_save_location()  # Get the save location from the user
    scaled_image.save(save_path)  # Save the image to the specified path
    print(f"Image saved to {save_path}")

    # Print total execution time
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
