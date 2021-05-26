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
def get_file_type(fileobj, relations: dict) -> str:
    name = fileobj.name
    extension = name.split(".")[-1:][0]

    for filetype in relations:
        if extension in relations[filetype]:
            return filetype

    c.print(f"Unknown ({extension}) - {name}")

    return "Unknown"


# Move file or directory
def moveobj(root, filename, filetype) -> None:
    dest = path.join(root, filetype)

    # Create the destination subfolder (Only the first time it is needed)
    if not path.exists(dest):
        os.mkdir(dest)

    # Move the files
    try:
        c.print(f"[underline white]{filename}[/underline white] [yellow]-> [bold purple]{filetype}")
        shutil.move(path.join(root, filename), path.join(dest, filename))
    except FileExistsError:
        c.print("Error moving " + filename + ", file already exists")


# Remove empty directories
def rm_empty(source):
    assert path.exists(source), "Path not found."

    done = False

    while not done:
        for root, subfolders, files in os.walk(source):
            if not len(list(os.scandir(root))):
                c.print("[red]Removing empty folder: " + root)
                os.rmdir(root)
                break
        else:
            done = True


# New main functionality
def filesort(folder: str, relations: dict) -> int:

    c.print(
        f"[bold red]Are you sure you want to run file_sort on folder [/bold red][underline bold yellow]'{folder}'[/underline bold yellow][bold red]?"
    )
    c.print("[bold red]Any files with the same names will be [underline]overwritten[/underline].")
    c.print("[cyan](Press ENTER to proceed or CTRL+C to exit)")

    try:
        input("")
    except KeyboardInterrupt:
        c.print("[yellow] -- Exited --")
        raise SystemExit(0)

    for obj in os.scandir(folder):
        root = path.dirname(obj.path)

        if obj.is_dir():
            if obj.name not in relations.keys():  # Avoid moving own folders
                moveobj(root, obj.name, "Folder")
            else:
                c.print(f"[yellow]Omitting '{obj.name}' folder")

        elif obj.is_file():
            filetype = get_file_type(obj, relations)
            moveobj(root, obj.name, filetype)

        else:  # Catch exception
            c.print("[bold red]Weird file found. Not folder neither file. ->" + obj.name)
            raise SystemExit(0)

    # Remove empty folders
    c.print("[bold blue]All files were sorted")
    c.print("[bold blue]Empty folders will now be removed")
    c.print("[cyan](Press ENTER to proceed or CTRL+C to exit)")
    try:
        input("")
    except KeyboardInterrupt:
        raise SystemExit(0)

    rm_empty(folder)

    return 0


if __name__ == "__main__":
    default_folder = os.getcwd()

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", help="Path to run the script on", default=default_folder)
    parser.add_argument(
        "-f",
        "--file",
        help="Path to the relations file (Defaults to project's folder)",
        default=path.join(os.getcwd(), "relations.json"),
    )

    args = parser.parse_args()
    folder, rel_file = args.path, args.file

    relations = get_relations(rel_file)

    if not filesort(folder, relations):
        c.print("[dim green]Job done :)")
