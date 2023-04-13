import os
import math
import shutil
from PIL import Image
import subprocess

# Define the compress_heic function here
def compress_heic(file_path, quality=80, output_extension='.jpg'):
    """
    Compresses a .heic file to an output file with the specified extension and quality.

    Arguments:
    file_path -- the path of the .heic file to compress
    quality -- the JPEG quality level (default is 80)
    output_extension -- the extension of the output file (default is '.jpg')

    Returns:
    The path of the compressed output file.
    """
    # Set up the output file path
    output_path = file_path.replace('.heic', output_extension)

    # Execute the heif-convert command to compress the file
    cmd = ['heif-convert', '-q', str(quality), file_path, output_path]
    subprocess.run(cmd, check=True)

    # Return the path of the compressed output file
    return output_path


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
            if extension in valid_extensions:

                # Check if the file is larger than the max size
                current_size = os.path.getsize(file_path)
                total_previous_file_size += current_size
                kb_size = current_size / 1000
                print('File size is ' + str(kb_size) + 'kb')
                if current_size > max_size:

                    # Open the image and calculate new dimensions that maintain the aspect ratio and result in a file size below the max size
                    if extension == '.heic':
                        compressed_file_path = compress_heic(file_path, quality=quality, output_extension='.heic')
                    else:
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

                    new_size = os.path.getsize(compressed_file_path)
                    total_current_file_size += current_size - new_size
                    print(f"{filename} compression completed successfully.")
                elif current_size < max_size and current_size > 0:
                    if extension == '.heic':
                        compressed_file_path = compress_heic(file_path, quality=quality, output_extension='.heic')
                    new_size = os.path.getsize(compressed_file_path)
                    total_current_file_size += current_size - new_size
                    print(f"{filename} compression completed successfully.")
                elif current_size < max_size and current_size > 0:
                    if extension == '.heic':
                        compressed_file_path = compress_heic(file_path, quality=quality, output_extension='.heic')
                    else:
                        # Open the image and copy it to the new folder with a new file name that includes the original file name and the "compressed" suffix
                        image = Image.open(file_path)
                        if compressedtitle == "YES":
                            compressed_file_name = f"{os.path.splitext(filename)[0]}_compressed{extension}"
                        else:
                            compressed_file_name = f"{os.path.splitext(filename)[0]}{extension}"
                        compressed_file_path = os.path.join(compressed_folder_path, compressed_file_name)
                        image.save(compressed_file_path)

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
