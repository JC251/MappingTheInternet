from def_func import ping_ip_range, create_image  # Import the functions from def_func.py
import os

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

def main():
    start_ip = input("Enter start IP (like 10.0.8.1): ")  # Change to your starting IP
    end_ip = input("Enter end IP (like 10.0.8.255): ")   # Change to your ending IP
    img_format = "D" #S for square, anything else for default fixed width

    ############testing############
    #start_ip = "1.1.250.0"
    #end_ip = "1.2.1.1"    

    width = 16 # Width of the image

    results = ping_ip_range(start_ip, end_ip)
    image = create_image(results, width, img_format)

    save_path = get_save_location()  # Get the save location from the user
    image.save(save_path)  # Save the image to the specified path
    print(f"Image saved to {save_path}")

if __name__ == "__main__":
    main()
