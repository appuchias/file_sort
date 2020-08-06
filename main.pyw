import json
import os
import sys
from os import path


class FileSort:
    default_folder = ""

    with open("relations.json") as r:
        relations = json.load(r)

    # Get everything inside the folder
    def get_dir_names(self, _dir):
        return [folder.name for folder in os.scandir(_dir)]

    # Get the file type through its extension
    def get_file_type(self, file):
        name = file.name
        extension = name.split(".")[-1:][0]

        for filetype in self.relations:
            if extension in self.relations[filetype]:
                return filetype

        print(f"Unknown ({extension}) - {name}")
        return "Unknown"

    # Remove empty directories
    def get_empty(self, source):
        assert path.exists(source), "Path not found."

        empty_folders = []

        for root, subfolders, files in os.walk(source):
            if not len(list(os.scandir(root))):
                print("Removing empty folder: " + root)
                empty_folders.append(root)
        
        return empty_folders
        

    # Main functionality
    def main(self):
        if len(sys.argv) > 1:
            folder = sys.argv[1]
        else:
            assert (
                len(self.default_folder) > 0
            ), "Please specify a default folder inside 'main.py'"  # Make sure it can run
            folder = self.default_folder

        for obj in os.scandir(folder):
            if obj.is_dir():
                if obj.name not in self.relations.keys() and obj.name not in [
                    "Folders",
                    "Unknown",
                ]:  # Avoid moving any unwanted folder
                    filepath = (
                        "\\".join(obj.path.split("\\")[:-1]) + "\\"
                    )  # Remove the folder name from the path
                    assert path.isdir(filepath)  # Avoid errors

                    if not os.path.exists(
                        filepath + "Folders\\"
                    ):  # Create the "Folders" folder in case it doesn't exist
                        os.mkdir(filepath + "Folders\\")

                    print(obj.name + " -> " + "Folders\\" + obj.name)
                    try:
                        os.rename(
                            obj.path, filepath + "Folders\\" + obj.name
                        )  # Move the folder into the "Folders" folder
                    except FileExistsError:
                        print("Error moving " + obj.name + ". File already exists")

                else:
                    print(f'Omitting "{obj.name}" folder')

            elif obj.is_file():
                filetype = self.get_file_type(obj)
                filepath = (
                    "\\".join(obj.path.split("\\")[:-1]) + "\\"
                )  # Remove the file name from its path
                assert path.isdir(filepath)  # Avoid errors
                if not os.path.exists(
                    filepath + filetype + "\\"
                ):  # Create the sub folder for the file type
                    os.mkdir(filepath + filetype + "\\")
                print(obj.name + " -> " + filetype)
                try:
                    os.rename(obj.path, filepath + filetype + "\\" + obj.name)
                except FileExistsError:
                        print("Error moving " + obj.name + ". File already exists")
        
        empty_folders = self.get_empty(folder)

        for folder in empty_folders:
            assert path.exists(folder), "Folder does not exist so it cannot be deleted"
            os.system("rmdir " + folder)


if __name__ == "__main__":
    file_sort = FileSort()
    file_sort.main()
