import os
import shutil
import datetime


def copyfoldertree():
    # Get the home directory
    home_dir = os.path.expanduser("~")

    # Create the source directory name
    today = datetime.date.today().strftime("%Y-%m-%d")
    source_dir_name = "uncompressed" + today
    source_dir = os.path.join(os.getcwd(), source_dir_name)

    # Create a new directory with the name "compressed" + today's date in the home directory
    base_dir_name = "compressed" + today
    destination_dir = os.path.join(os.getcwd(), base_dir_name)

    if os.path.exists(destination_dir):
        i = 0
        while True:
            i += 1
            new_dir_name = base_dir_name + "_" + str(i).zfill(2)
            new_destination_dir = os.path.join(home_dir, new_dir_name)
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
