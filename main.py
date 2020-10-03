import json
import os
import shutil
import sys
from os import path
from time import sleep

from colorama import Fore, init
init()

default_folder = ""

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
        print("Error moving " + filename + ". Already exists")

# Remove empty directories
def rm_empty(source):
    assert path.exists(source), "Path not found."

    for root, subfolders, files in os.walk(source):
        if not len(list(os.scandir(root))):
            print(Fore.RED + "Removing empty folder: " + root + Fore.WHITE)
            os.rmdir(root)


# New main functionality
def main():
    if len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        assert (len(default_folder) > 0), "Please specify a default folder inside 'improved.pyw'" # Make sure it can run
        folder = default_folder


    print(Fore.RED + "Are you sure you want to run file_sort on folder '" + folder + "'?")
    print(Fore.RED + "Any files with the same names will be overwritten.")
    print(Fore.CYAN + "(Press ENTER to proceed or CTRL+C to exit)" + Fore.WHITE)

    try:
        input()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n -- Exited -- \n")
        sys.exit(0)


    for obj in os.scandir(folder):
        root = path.dirname(obj.path)

        if obj.is_dir():
            if obj.name not in relations.keys() and obj.name not in ["Folder", "Unknown"]:
                moveobj(root, obj.name, "Folder")
            else:
                print(Fore.YELLOW + "Omitting '" + obj.name + "' folder" + Fore.WHITE)

        elif obj.is_file():
            moveobj(root, obj.name, get_file_type(obj))

        else:
            print(Fore.RED + "Weird file found. Not folder neither file. " + obj.name + Fore.WHITE)

    # Remove empty folders
    rm_empty(folder)

    print("\n" + Fore.GREEN + "Job done :)")



if __name__ == "__main__":
    main()
    sleep(2)
