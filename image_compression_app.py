import os
import math
import datetime
from PIL import Image
import shutil
# import pyheif
import subprocess

def copyfoldertree(folderpath):
    # Get the home directory
    home_dir = os.path.expanduser("~")

    # Create the source directory name
    today = datetime.date.today().strftime("%Y-%m-%d")
    source_dir = folderpath
    source_dir_name = os.path.dirname()
    source_dir_folder_path = source_dir.replace(source_dir_name, '')

    # Create a new directory with the name "compressed" + today's date in the home directory
    base_dir_name = source_dir_name + '_compressed' + today
    destination_dir = source_dir_folder_path + base_dir_name

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

def heic_to_jpeg(file_path):
    """
    Converts a .heic file to a .jpeg file.

    Arguments:
    file_path -- the path of the source .heic file

    Returns:
    The path of the converted .jpeg file.
    """
    # Define the output file path with the same file name, but with the .jpeg extension
    jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'

    # Execute the heif-convert command to convert the file
    cmd = ['heif-convert', file_path, jpeg_path]
    subprocess.run(cmd, check=True)

    # Return the path of the converted .jpeg file
    return jpeg_path


def jpeg_to_heic(file_path):
    """
    Converts a .jpeg file to a .heic file using the sips command-line tool.

    Arguments:
    file_path -- the path of the .jpeg file to convert

    Returns:
    The path of the converted .heic file.
    """
    # Define the output file path with the same file name, but with the .heic extension
    heic_path = os.path.splitext(file_path)[0] + '.heic'

    # Execute the sips command to convert the file
    cmd = ['sips', '-s', 'format', 'heic', file_path, '--out', heic_path]
    subprocess.run(cmd, check=True)

    # Return the path of the converted .heic file
    return heic_path

def delete_jpeg(file_path):
    """
    Deletes a .jpeg file.

    Arguments:
    file_path -- the path of the .jpeg file to delete

    Returns:
    None
    """
    # Define the corresponding .heic file path
    heic_path = os.path.splitext(file_path)[0] + '.heic'
    jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'

    # Check if the corresponding .heic file exists
    if os.path.exists(heic_path):
        # If the .heic file exists, delete the .jpeg file
        os.remove(jpeg_path)
    else:
        # If the .heic file does not exist, do nothing
        pass

def compress_images_directory(directory_name, compressed_folder_path, compressedtitle='YES', max_size=1048576, quality=85):
    # Define a list of valid image extensions
    valid_extensions = ['.jpeg', '.jpg', '.png', '.webp', '.heic']

    total_previous_file_size = 0
    total_current_file_size = 0

    # Loop over all files in the specified directory
    for filename in os.listdir(directory_name):
        file_path = os.path.join(directory_name, filename)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):

            # Check if the file has a valid image extension
            extension = os.path.splitext(file_path)[1].lower()
            old_extension = os.path.splitext(file_path)[1].lower()
            if extension in valid_extensions:

                # Check if the file is larger than the max size
                current_size = os.path.getsize(file_path)
                total_previous_file_size += current_size
                kb_size = current_size / 1000
                print('File size is ' + str(kb_size) + 'kb')
                if current_size > max_size:

                    # Open the image and calculate new dimensions that maintain the aspect ratio and result in a file size below the max size
                    if extension == '.heic':
                        file_path = heic_to_jpeg(file_path)
                        filename = file_path.replace(directory_name + '/', '')
                        extension = os.path.splitext(file_path)[1].lower()
                    #     compressed_file_path = compress_heic(file_path, quality=quality, output_extension='.heic')
                    # else:
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

                    if old_extension == '.heic':
                        compressed_file_path = jpeg_to_heic(compressed_file_path)
                        delete_jpeg(file_path)
                        delete_jpeg(compressed_file_path)

                    new_size = os.path.getsize(compressed_file_path)
                    total_current_file_size += current_size - new_size
                    print(f"{filename} compression completed successfully.")

                elif current_size < max_size and current_size > 0:
                    # Open the image and copy it to the new folder with a new file name that includes the original file name and the "compressed" suffix
                    
                    if extension == '.heic':
                        file_path = heic_to_jpeg(file_path)
                        filename = file_path.replace(directory_name + '/', '')
                        extension = os.path.splitext(file_path)[1].lower()
                    
                    image = Image.open(file_path)
                    
                    if compressedtitle == "YES":
                        compressed_file_name = f"{os.path.splitext(filename)[0]}_compressed{extension}"
                    else:
                        compressed_file_name = f"{os.path.splitext(filename)[0]}{extension}"
                    
                    compressed_file_path = os.path.join(compressed_folder_path, compressed_file_name)
                    
                    image.save(compressed_file_path)
                    
                    if old_extension == '.heic':
                        compressed_file_path = jpeg_to_heic(compressed_file_path)
                        delete_jpeg(file_path)
                        delete_jpeg(compressed_file_path)

                    
                    total_current_file_size += 0
                    print(f"{filename} copied to compressed folder.")
                elif current_size == 0:
                    continue
            else:
                # Copy the file to the compressed folder path if the extension is not valid
                compressed_file_name = f"{os.path.splitext(filename)[0]}{extension}"
                compressed_file_path = os.path.join(compressed_folder_path, compressed_file_name)
                shutil.copy(file_path, compressed_file_path)
                print(f"{filename} copied to compressed folder.")

    # Print the total size of all files and the total size savings
    total_previous_file_size_kb = total_previous_file_size / 1000
    total_current_file_size_kb = total_current_file_size / 1000
    print(f"All files in the directory are {total_previous_file_size_kb}kb in total.")
    print(f"The total file size savings are {total_current_file_size_kb}kb.")
    
    return [total_previous_file_size, total_current_file_size]



def compress_images_all(compresseddirname="", compressedtitle="YES", max_size=1048576, quality=85):
        # Get the home directory
    home_dir = os.path.expanduser("~")
    total_file_size = 0
    total_file_savings = 0

    # Create the source directory name
    today = datetime.date.today().strftime("%Y-%m-%d")
    source_dir_name = "compression/" + "uncompressed" + today
    source_dir = os.path.join(os.getcwd(), source_dir_name)

    destination_dir = os.path.join(os.getcwd(), compresseddirname)

    # Walk through the source directory and call compress_images_all() on each directory
    for root, dirs, files in os.walk(source_dir):
        for dir in dirs:
            # Call compress_images_all() on the directory
            file_sizes_list = compress_images_directory(os.path.join(root, dir), os.path.join(root.replace(source_dir, destination_dir), dir), compressedtitle, max_size, quality)
            
            total_file_size += file_sizes_list[0]
            total_file_savings += file_sizes_list[1]
    current_file_size = total_file_size - total_file_savings
    total_file_savings_mb = total_file_savings / 1000000
    current_file_size_mb = current_file_size / 1000000
    total_file_size_mb = total_file_size /1000000
    print("Original File is " + str(total_file_size_mb) + "mb")
    print("Current File is " + str(current_file_size_mb) + "mb")
    print("File Savings are " + str(total_file_savings_mb) + "mb")
    
    print("Directory structure copied and images compressed successfully to", destination_dir)


# folderpath = mac input

# Call the function to copy the folder tree
compressed_dir_name = copyfoldertree(folderpath=)
# Call the cuntion to compress all the images of a folder tree
compress_images_all(compresseddirname=compressed_dir_name,compressedtitle="NO", max_size=1048576, quality=95)

