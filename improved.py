import json
import os
import shutil
import sys
from os import path

from colorama import Fore

default_folder = "/home/pi/Downloads"

# Get extension type relationships
with open("relations.json") as r:
    relations = json.load(r)

# Get the file type through its extension
def get_file_type(file):
    name = file.name
    extension = name.split(".")[-1:][0]

    for filetype in relations:
        if extension in relations[filetype]:
            return filetype

    print(f"Unknown ({extension}) - {name}")
    return "Unknown"


# Move file or directory
def moveobj(root, filename, filetype):
    dest = path.join(root, filetype)

    # Create the destination subfolder (Only the first time it is needed)
    if not path.exists(dest):
        os.mkdir(dest)

    # Move the files
    try:
        print(filename + " -> " + filetype)
        shutil.move(path.join(root, filename), path.join(dest, filename))
    except FileExistsError:
        print("Error moving " + obj.name + ". Already exists")

# Get empty directories
def get_empty(source):
    assert path.exists(source), "Path not found."

    empty_folders = []

    for root, subfolders, files in os.walk(source):
        if not len(list(os.scandir(root))):
            print("Removing empty folder: " + root)
            empty_folders.append(root)

    return empty_folders


# New main functionality
def main():
    if len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        assert (len(default_folder) > 0), "Please specify a default folder inside 'improved.pyw'" # Make sure it can run
        folder = default_folder

    for obj in os.scandir(folder):
        root = path.dirname(obj.path)

        if obj.is_dir():
            if obj.name not in relations.keys() and obj.name not in ["Folder", "Unknown"]:
                moveobj(root, obj.name, "Folder")
            else:
                print("Omitting '" + obj.name + "' folder")

        elif obj.is_file():
            moveobj(root, obj.name, get_file_type(obj))

        else:
            print("Weird")

    print("Job done :)")



if __name__ == "__main__":
    try:
        print(Fore.RED + "Are you sure you want to run file_sort on folder '" + default_folder + "'?")
        print(Fore.RED + "Any files with the same names will be overwritten.")
        print(Fore.CYAN + "(Press ENTER to proceed or CTRL+C to exit)" + Fore.WHITE)
        input()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n -- Exited -- \n")
        sys.exit(0)
    main()
