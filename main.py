import sys, os, json

default_folder = ""

def get_dir_names(dir):
    return [folder.name for folder in os.scandir(dir)]


def get_file_type(file):
    name = file.name
    extension = name.split(".")[-1:][0]
    
    with open("relations.json") as r:
        relations = json.load(r)
    
    for type in relations:
        if extension in relations[type]:
            return type
    
    print(f"Unknown ({extension}) - {name}")
    return "Unknown"


if len(sys.argv) > 1:
    for obj in os.scandir(sys.argv[1]):
        if obj.is_file():
            print(obj.name + " -> " + get_file_type(obj))
else:
    assert len(default_folder) > 0, "Please specify a default folder inside 'main.py'"
    for obj in os.scandir(default_folder):
        if obj.is_file():
            print(obj.name + " -> " + get_file_type(obj))
