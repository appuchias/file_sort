import os
from os import path
import json
import shutil
import argparse

from rich.console import Console

c = Console()


# Get the relations file from any path
def get_relations(filepath: str) -> dict:
    assert path.exists(filepath), "Specified relations file does not exist"
    with open(filepath) as r:
        relations = json.load(r)

    return relations


# Get the file type through its extension
def get_file_type(file):
    name = file.name
    extension = name.split(".")[-1:][0]

    for filetype in relations:
        if extension in relations[filetype]:
            return filetype

    c.print(f"Unknown ({extension}) - {name}")
    return "Unknown"


# Move file or directory
def moveobj(root, filename, filetype):
    dest = path.join(root, filetype)

    # Create the destination subfolder (Only the first time it is needed)
    if not path.exists(dest):
        os.mkdir(dest)

    # Move the files
    try:
        c.print(f"[underline white]{filename}[/underline] [yellow]-> [bold purple]{filetype}")
        shutil.move(path.join(root, filename), path.join(dest, filename))
    except FileExistsError:
        c.print("Error moving " + filename + ", file already exists")


# Remove empty directories
def rm_empty(source):
    assert path.exists(source), "Path not found."

    for root, subfolders, files in os.walk(source):
        if not len(list(os.scandir(root))):
            c.print("[red]Removing empty folder: " + root)
            os.rmdir(root)


# New main functionality
def filesort(folder):

    c.print(
        f"[bold red]Are you sure you want to run file_sort on folder [/bold red][underline bold yellow]'{folder}'[/underline bold yellow][bold red]?"
    )
    c.print("[bold red]Any files with the same names will be [underline]overwritten[/underline].")
    c.print("[bold light blue]Empty folders will also be removed")
    c.print("[cyan](Press ENTER to proceed or CTRL+C to exit)")

    try:
        input()
    except KeyboardInterrupt:
        c.print("[yellow] -- Exited --\n")
        sys.exit(0)

    for obj in os.scandir(folder):
        root = path.dirname(obj.path)

        if obj.is_dir():
            if obj.name not in relations.keys():
                moveobj(root, obj.name, "Folder")
            else:
                c.print(f"[yellow]Omitting '{obj.name}' folder")

        elif obj.is_file():
            moveobj(root, obj.name, get_file_type(obj))

        else:  # Catch exception
            c.print("[bold red]Weird file found. Not folder neither file. ->" + obj.name)
            sys.exit(0)

    # Remove empty folders
    rm_empty(folder)

    c.print("\n[dim green]Job done :)")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        assert (
            len(default_folder) > 0
        ), "Please specify a default folder inside the '.py' file."  # Make sure it can run
        folder = default_folder

    filesort(folder)
