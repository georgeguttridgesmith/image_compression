import os
import math
import datetime
from PIL import Image
import shutil


def copyfoldertree():
    # Get the home directory
    home_dir = os.path.expanduser("~")

    # Create the source directory name
    today = datetime.date.today().strftime("%Y-%m-%d")
    source_dir_name = "compression/" + "uncompressed" + today
    source_dir = os.path.join(os.getcwd(), source_dir_name)

    # Create a new directory with the name "compressed" + today's date in the home directory
    base_dir_name = "compression/" + "compressed" + today
    destination_dir = os.path.join(os.getcwd(), base_dir_name)

    if os.path.exists(destination_dir):
        i = 0
        while True:
            i += 1
            new_dir_name = base_dir_name + "_" + str(i).zfill(2)
            base_dir_name = new_dir_name
            new_destination_dir = os.path.join(os.getcwd(), new_dir_name)
            if not os.path.exists(new_destination_dir):
                destination_dir = new_destination_dir
                os.mkdir(destination_dir)
                break
    else:
        os.mkdir(destination_dir)

    # Recursively create the same directory structure in the destination directory
    for root, dirs, files in os.walk(source_dir):
        for dir in dirs:
            path = os.path.join(destination_dir, root.replace(source_dir_name, base_dir_name), dir)
            if not os.path.exists(path):
                os.makedirs(path)
                os.chmod(path, 0o700)

    print("Directory structure copied successfully to", destination_dir)
    return base_dir_name

def compress_images_directory(directory_name, compressed_folder_path, compressedtitle='YES', max_size=1048576, quality=85):
    # Define a list of valid image extensions
    valid_extensions = ['.jpeg', '.jpg', '.png', '.heic', '.webp']

    # Loop over all files in the specified directory
    for filename in os.listdir(directory_name):
        file_path = os.path.join(directory_name, filename)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):

            # Check if the file has a valid image extension
            extension = os.path.splitext(file_path)[1].lower()
            if extension in valid_extensions:

                # Check if the file is larger than the max size
                current_size = os.path.getsize(file_path)
                kb_size = current_size / 1000
                print('File size is ' + str(kb_size) + 'kb.')
                if current_size > max_size:

                    # Open the image and calculate new dimensions that maintain the aspect ratio and result in a file size below the max size
                    image = Image.open(file_path)
                    width, height = image.size
                    aspect_ratio = width / height
                    new_width = math.sqrt(max_size * aspect_ratio)
                    new_height = new_width / aspect_ratio
                    new_dimensions = (int(new_width), int(new_height))

                    # Compress the image with the specified quality level and save it to the new folder with a new file name that includes the original file name and the "compressed" suffix
                    image = image.resize(new_dimensions, Image.ANTIALIAS)
                    if compressedtitle == "YES":
                        compressed_file_name = f"{os.path.splitext(filename)[0]}_compressed{extension}"
                    else:
                        compressed_file_name = f"{os.path.splitext(filename)[0]}{extension}"
                    compressed_file_path = os.path.join(compressed_folder_path, compressed_file_name)
                    image.save(compressed_file_path, optimize=True, quality=quality)

                    print("Image compression completed successfully.")
            else:
                print("Image compression not completed.")

def compress_images_all(compresseddirname="", compressedtitle="YES", max_size=1048576, quality=85):
        # Get the home directory
    home_dir = os.path.expanduser("~")

    # Create the source directory name
    today = datetime.date.today().strftime("%Y-%m-%d")
    source_dir_name = "compression/" + "uncompressed" + today
    source_dir = os.path.join(os.getcwd(), source_dir_name)

    destination_dir = os.path.join(os.getcwd(), compresseddirname)

    # Walk through the source directory and call compress_images_all() on each directory
    for root, dirs, files in os.walk(source_dir):
        for dir in dirs:
            # Call compress_images_all() on the directory
            compress_images_directory(os.path.join(root, dir), os.path.join(root.replace(source_dir, destination_dir), dir), compressedtitle, max_size, quality)

    print("Directory structure copied and images compressed successfully to", destination_dir)




# Call the function to copy the folder tree
compressed_dir_name = copyfoldertree()
# Call the cuntion to compress all the images of a folder tree
compress_images_all(compresseddirname=compressed_dir_name,compressedtitle="NO", max_size=1048576, quality=95)
